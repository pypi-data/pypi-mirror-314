# -*- coding: utf-8 -*-
# @Author: Vivian Li
# @Date:   2024-01-29 13:26:17
# @Last Modified by:   Vivian Li
# @Last Modified time: 2024-04-06 23:58:52
# @Description: A plugin suite contains multiple plugins. A PluginSuite
# object stores every information about a suite, including the dependencies between
# each plugins, suite metadata , suite documentation path, suite format markdown path.
# When itself is called, it execute procedure to run the suite.
import sys
import os
from collections import defaultdict
from typing import Dict, List, Any, Tuple, Optional
import subprocess
import os.path


import xml.etree.ElementTree as ET

from gailbot.shared.exception.serviceException import FailPluginSuiteRegister
from gailbot.pluginSuiteManager.error.errorMessage import SUITE_REGISTER_MSG
from gailbot.pluginSuiteManager.suite.gbPluginMethod import GBPluginMethods
from gailbot.configs import PLUGIN_CONFIG
from gailbot.pluginSuiteManager.suite.pluginData import Suite, ConfModel, Requirements, Dependencies
from gailbot.shared.pipeline import (
    Pipeline,
)
from gailbot.shared.utils.general import get_name

import importlib

from gailbot.pluginSuiteManager.suite.pluginComponent import PluginComponent
from gailbot.shared.utils.logger import makelogger
from gailbot.shared.utils.general import read_toml
from gailbot.workspace.manager import WorkspaceManager
from gailbot.workspace.directory_structure import OutputFolder

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from RDS_connect import RDSClient
from S3BucketManager import S3BucketManager
from userpaths import get_profile


USER = get_profile()

logger = makelogger("plugin suite")


class PluginSuite:
    """
    Manages a suite of plugins and responsible for loading, queries, and
    execution.
    Needs to store the details of each plugin (source file etc.)
    """

    def __init__(self, conf_model: ConfModel, root: str):
        """a dictionary of the dependency map  -> transcriptionPipeline argument"""
        self.suite_name = conf_model.suite.name
        self.conf_model = conf_model
        self.source_path = root
        self.optional_plugins: List[str] = []
        self.required_plugins: List[str] = []
        self.workspace = WorkspaceManager()
        self.workspace.init_workspace()
        # suite and document_path will be loaded in _load_from_config
        self.suite = conf_model.suite
        self.formatmd_path = os.path.join(root, self.suite_name, PLUGIN_CONFIG.FORMAT)
        self.dependency_map, self.plugins = self._load_from_config(conf_model, root)

        # self.download_plugins(plugin_ids= self.plugins)

        # Add vars here from conf.
        self._is_ready = True
        self.is_official = False

    @property
    def name(self) -> str:
        return self.suite_name

    @property
    def is_ready(self):
        return self._is_ready

    def set_to_official_suite(self):
        """set the plugin to official plugin"""
        self.is_official = True

    def __repr__(self):
        return (
            f"Plugin Suite: {self.name}\n" f"Dependency map: {self.dependency_graph()}"
        )

    def __call__(
        self,
        base_input: Any,
        methods: GBPluginMethods,
        selected_plugins: Optional[Dict[str, List[str]] | List[str]] = None, #check which type is currently being used
    ) -> Dict:
        """
        Apply the specified plugins when possible and return the results
        summary
        """

        selected_plugins = self.plugins
        output_path = OutputFolder(methods.out_path)
        
        print(selected_plugins)

        # Check temp dir and save selected dag
        adj_list = {k: v for k, v in self.dependency_map.items() if k in selected_plugins}
        #
        print(adj_list)
        dag = self._topological_sort(adj_list)
        print("DAG", ', '.join(dag))

        host_path = os.path.join(self.workspace.plugins, "0", "1.0")


        if not os.path.isdir(os.path.join(host_path, "transcript")):
            os.makedirs(os.path.join(host_path, "transcript"))

        dag_path = os.path.join(host_path, "transcript", "dag.txt")

        with open(dag_path, "w") as f:
            f.write(' '.join(dag))

        # Save transcript to plugin 0 folder and to final output folder
        transcript_path = os.path.join(host_path, "transcript", "original_data.txt") 
        xml = self._convert_to_xml(methods.utterances)
        
        with open(transcript_path, "w") as f:
            f.write(ET.tostring(xml, encoding="unicode", method="xml"))

        transcript_out_path = os.path.join(output_path.transcribe, "original_trancript.xml")
        with open(transcript_out_path, "w") as f:
            f.write(ET.tostring(xml, encoding="unicode", method="xml"))


        if not os.path.exists(transcript_path):
            print("transcript path doesnt exist")

        print("Selected plugins are ", selected_plugins)
        # self.download_plugins(plugin_ids= selected_plugins)
        
        env = os.environ.copy()
        env["OUTPUT"] = methods.work_path
        env["NAME"] = "testing" + str(0)
        compose_file = os.path.join(self.source_path, self.suite_name, "plugin_suite_compsed.yaml")
        command = ['docker-compose', '-f', compose_file, '-p', "testing" + str(0), 'up', '--build',]
        result = subprocess.run(command, env=env, text=True)
    

        command = ['docker-compose', '-p', "testing" + str(0), 'wait']  # Wait for all containers to finish
        subprocess.run(command, env=env, text=True)

        if result.returncode != 0:
            print("Docker Compose failed with exit code:", result.returncode)
        else:
            print("Docker Compose ran successfully")
            
        final_result_file = os.path.join(methods.work_path, f"plugin_{dag[-1]}_result.xml")
        if not os.path.isfile(final_result_file):
            print(f"Error: did not find temp result file corresponding to final plugin {id}.")
        else:
            # assuming output_path leads to result_directory/analysis/suite_name/ 
           
            with open(final_result_file, 'r') as source_file:
                res = source_file.read()
                
            output_file = os.path.join(output_path.analysis, "final_plugin_result.xml")
            if not os.path.is_file(output_file):
                os.makedirs(output_file)
                
            with open(output_file, "w") as target_file:
                target_file.write(res)
                
                
    def is_plugin(self, plugin_name: str) -> bool:
        """given a name , return true if the plugin is in the plugin suite"""
        return plugin_name in self.plugins

    def plugin_names(self) -> List[str]:
        """Get names of all plugins"""
        return list(self.plugins.keys())

    def dependency_graph(self) -> Dict:
        """Return the entire dependency graph as a dictionary"""
        return self.dependency_map

    def get_meta_data(self) -> Suite:
        """get the metadata about this plugin"""
        return self.suite

    # def download_plugins(self, methods: GBPluginMethods, plugin_ids: List[str]):
    #     s3 = S3BucketManager()
    #     rds = RDSClient()
    #     rds.connect()
    #     for plugin in plugin_ids:
    #         print("work path is: ", methods.work_path, "plugin id is: ", plugin)
    #         s3_url = rds.fetch_plugin_s3_url(plugin_id= plugin)
    #         print("s3 url is: ", s3_url)
    #         # prefix needs to be user -> plugins -> plugin id
    #         s3.download_plugins(bucket= "gailbot-plugins", prefix= s3_url, local_dir= methods.work_path)

    #     rds.close_connection()


    ##########
    # PRIVATE
    ##########
    def _load_from_config(
        self, conf_model: ConfModel, root: str
    ) -> Tuple[Dict[str, List[str]], Dict[str, str]] | None:
        """
        load the plugin suite, the information about each plugin name,
        and its path is stored in the dict_config, all path information
        is relative to the abs_path

        Parameters
        ----------
        conf_model: stores the plugin suite data for suite registration
        root: the path to the root folder of the plugin suite source code

        """
        plugins: Dict[str, str] = dict()

        plugin_entries = conf_model.suite.plugins.split(' ')

        for plugin_id in plugin_entries:
            plugin_path = os.path.join(self.workspace.plugins, plugin_id, "1.0")
            plugins[plugin_id] = plugin_path
        

        self.download_plugins(plugin_ids = plugin_entries)
        
        dependency_map: Dict[str, List[str]] = self._create_adjacency_list(plugins)


        return (
            dependency_map,
            plugins,
        )  
    

    def _create_adjacency_list(self, plugins_data: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Create an adjacency list from the list of plugin data.

        Args:
        - plugins_data: List of dictionaries containing plugin information.

        Returns:
        - Dict: An adjacency list where keys are plugin names and values are lists of dependencies.
        """
        adjacency_list = {}
        for plugin_id, plugin_path in plugins_data.items():
            if (plugin_id != "0"):
                toml_file_path = os.path.join(plugin_path, "plugin_info.toml")
                

                plugin_info = read_toml(toml_file_path)

                adjacency_list[plugin_id] = list(plugin_info.get('requirements', {}).values())
            else:
                adjacency_list[plugin_id] = []
                    

        return adjacency_list
    

    def _convert_to_xml(self, data):
        root = ET.Element("transcript")
        
        current_speaker = None
        current_u = None
        
        for data in data.values():
            for item in data:
                print(item)
                if item['speaker'] != current_speaker:
                    current_speaker = item['speaker']
                    current_u = ET.SubElement(root, "u", speaker=current_speaker)
                
                word = ET.SubElement(current_u, "w", start=str(item['start']), end=str(item['end']))
                word.text = item['text']

        return root



    
    def _topological_sort(self, adj_list):
        # Initialize the graph and in-degree dictionary
        graph = {}
        in_degree = {}

        # Build the graph and compute in-degrees of each node
        for node in adj_list:
            if node not in graph:
                graph[node] = []
            if node not in in_degree:
                in_degree[node] = 0
            for dep in adj_list[node]:
                if dep not in graph:
                    graph[dep] = []
                graph[dep].append(node)
                if node not in in_degree:
                    in_degree[node] = 0
                in_degree[node] += 1

        # Find all nodes with in-degree 0
        queue = []
        for node in in_degree:
            if in_degree[node] == 0:
                queue.append(node)
        
        order = []

        # Process nodes with in-degree 0 and update the in-degrees of their neighbors
        while queue:
            current = queue.pop(0)
            order.append(current)
            for neighbor in graph[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check if there was a cycle
        if len(order) == len(in_degree):
            return order
        else:
            raise ValueError("A cycle was detected in the dependencies")



    
    def _separate_plugins(self, adj_list):
        # Create dictionaries to store the counts of incoming and outgoing edges
        outgoing_edges = defaultdict(set)
        incoming_edges = defaultdict(set)
        
        # Populate the dictionaries with the adjacency list information
        for plugin, dependencies in adj_list.items():
            outgoing_edges[plugin].update(dependencies)
            for dep in dependencies:
                incoming_edges[dep].add(plugin)
        
        # Find independent and required plugins
        self.optional_plugins = [plugin for plugin in outgoing_edges if plugin not in incoming_edges]
        self.required_plugins = [plugin for plugin in incoming_edges]
        


    def sub_dependency_graph(
        self, selected: List[str]
    ) -> Optional[Dict[str, List[str]]]:
        """
        given a selected list of plugins, return a subgraph of the dependency graph that
        include only the required plugin and the list of selected plugin

        Parameters
        ----------
        selected

        Returns
        -------

        """
        selected.extend(self.required_plugins)
        selected = set(selected)
        new_dependency = dict()
        for key, dependency in self.dependency_map.items():
            if key in selected:
                new_dependency[key] = list(
                    filter(lambda elt: elt in selected, dependency)
                )
        if not self.__check_dependency(new_dependency):
            logger.error(f"cannot resolve dependency for graph {new_dependency}")
        return new_dependency

    def __check_dependency(self, graph: Dict[Any, List[Any]]):
        """

        Parameters
        ----------
        graph

        Returns None
        -------

        Raises
        -------
        FailPluginSuiteRegister

        """
        visited = {k: 0 for k in graph.keys()}

        def check_circle(node: Any):
            visited[node] = -1
            for dependency in graph[node]:
                if visited[dependency] == -1:
                    raise FailPluginSuiteRegister(
                        self.suite_name,
                        SUITE_REGISTER_MSG.FAIL_LOAD_PLUGIN.format(
                            plugin=node,
                            cause=f" cannot resolve dependency {dependency} for plugin {node}",
                        ),
                    )
                elif visited[dependency] == 0:
                    if check_circle(dependency):
                        raise FailPluginSuiteRegister(
                            self.suite_name,
                            SUITE_REGISTER_MSG.FAIL_LOAD_PLUGIN.format(
                                plugin=node,
                                cause=f" cannot resolve dependency {dependency} for plugin {node}",
                            ),
                        )
            visited[node] = 1

        for node in graph.keys():
            check_circle(node)

        return True
    def download_plugins(self, plugin_ids: List[str]):
        s3 = S3BucketManager()
        rds = RDSClient()
        rds.connect()
        for plugin in plugin_ids:
            if plugin != '0':
                plugin_info = rds.fetch_plugin_info(plugin_id= plugin)
                # user_id = plugin_info["user_id"]
                # plugin_name = plugin_info["name"]
                version = plugin_info["version"]
                
                plugin_url = plugin_info["s3_url"]
                base_url = "https://gailbot-plugins.s3.us-east-2.amazonaws.com/"
                prefix = plugin_url.replace(base_url, "")

                
                local_dir = os.path.join(self.workspace.plugins, plugin, version)
                if not os.path.isdir(local_dir):
                    os.makedirs(local_dir)
                if not os.listdir(local_dir):
                    s3.download_plugin(bucket_name= "gailbot-plugins", prefix= prefix, local_dir= local_dir)
                    print("downloaded ", prefix, " from S3 into local path ", local_dir)
                else: # print statement j for debugging
                    print(f"local directory ({local_dir}) is not empty, already contains plugin files")
        rds.close_connection()

# def download_docker_from_S3():
