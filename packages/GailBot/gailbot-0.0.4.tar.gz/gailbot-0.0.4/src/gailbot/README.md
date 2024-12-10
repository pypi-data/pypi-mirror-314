# Terms 
- Engine
  - Refers to speech to text engine that convert conversation audio files to text content
- Plugin 
  - A class that implements one method or algorithm to post-process the output from speech to text transcription
- Plugin Suite 
  - A set of plugins. 
- Profile 
  - Store setting data for speech to text engine and selected plugin suite.
- Payload 
  - Stores different types of origin input into a consistent interface.
- Source
  - Initial raw input from users, can contain various input formats.
  
# Top-level Directory Structure 
- environment-setup 
  > contain environmental file for api environment
- sample 
  > sample code for ways to use gailbot API 
- src
  - gailbot 
    > gailbot source code 
  - test 
    > unit test for gailbot 
- test 
  - part of unit test for gailbot, (WARNING: this test suite has not been maintained and updated) 
  
# GailBot Module Structures
- api.py
- config_backend
  > Toml configuration files 
- configs
  > Parser for parsing toml file into python dataclasses
- engineManager
  > Manage engine settings, create stt engine, validate engine setting
    - engine
      > Adapter classes that provide consistent interfaces on top of third party stt engine. Each engine module
      implements their own interface for engine setting and engine provider. <br/> EngineSetting is a data-class that defines the structure of the setting data. 
      <br/> EngineProvider takes in raw engine setting, validate setting and include method
      to create the engine of that setting.
        - google
        - watson
        - whisper
        - whisperX (an improvement from whisper engine)
    - engineProvider.py
      > Abstract class for engineProvider
    - engineManager.py
      > Implementation of engine manager 

- pluginSuiteManger
    - error
      > Report error when loading pluginSuite
    - suite
    - suiteLoader
      > Load the pluginSuite from different types of sources
    - pluginMethod.py
      > When each Plugin is applied, it takes in a pluginMethod instance, which provides data from payload
    - pluginSuiteManager.py
      > Manage the registration, deletion of plugin suite

- profileManager
  > Manage the creation and deletion of gailbot profile <br/> ProfileManager depends on EngineManager and PluginManager

- sourceManager
    - sourceManager
    - sourceObject
      > Stores the raw source data

- payload
  > converting different formats of raw source to payload with consistent interface
  - payloadConverter
    > implement classes and functions to convert a source to PayloadObject
  - payloadObject
    > defines different types of payloadObject, there are TranscribedDirPayload
      and UntranscribedDirPayload, both are sub-classes for PayloadObject  

- transcriptionPipeline
  > Process the transcription process
    - converter
      > Converts source object to payload objects
        - payload
          > Payload takes in source object and its profile, implement start_execute method, which transcribe the files
          through stt_transcribe (previously refers to transcribe), analysis and format stages
        - result
          > Manage the result at each transcription phase 
          - sttTranscribe.py 
            > Manage the result returned from stt engine (previously named to transcribe.py)
          - analysis.py
            > Manage the result returned from plugin suite analysis, currently only stores the result of running each plugin (success or failure)
          - format.py
            > Export any metadata related with gailbot, currently only export a format.md file that documents the output directory structure 
    - pipeline.py
      > Takes in a list of tuples of sources and profiles, convert to payloads and start executing the transcription. 

- shared
  > Utility modules
    - exception
      - serviceException.py
        > Defines a list of exception classes raised outside a transcription process
      - transcribeException.py
        > Defines a list of exception classes raised during the transcription process
    - pipeline
      > A "smart" pipeline that is able to run components concurrently based on their dependencies
    - utils

- workspace
  > Managing gailbot workspace

