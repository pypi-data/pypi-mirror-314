import os.path
import unittest

from gailbot import GailBot, ProfileSetting


class TestGailbotSuiteFunction(unittest.TestCase):
    under_test = GailBot()
    output = "/Users/yike/Desktop/gbtest/output"
    source_root = "/Users/yike/Desktop/gbtest/input"
    small_source = os.path.join(source_root, "hello2.wav")
    test_2ab = os.path.join(source_root, "test2ab")

    def test_existing_suite(self):
        print(self.under_test.available_suites())
        print(self.under_test.get_selectable_plugins("HiLabSuite"))

    def test_all_plugin(self):
        all_selected_plugin = self.under_test.get_selectable_plugins("HiLabSuite")
        profile = ProfileSetting(
            engine_setting_name="Default",
            plugin_suite_setting={"HiLabSuite": all_selected_plugin}
        )
        self.plugin_suite_transcription_test(profile)

    def test_partial_plugin(self):
        selected_plugin = ['GapPlugin', 'PausePlugin', 'OverlapPlugin', 'TextPlugin', 'XmlPlugin', 'ChatPlugin']
        profile = ProfileSetting(
            engine_setting_name="Default",
            plugin_suite_setting={"HiLabSuite": selected_plugin}
        )
        self.plugin_suite_transcription_test(profile)

    def test_name_not_found_suite(self):
        self.plugin_suite_register_err_test(os.path.join(self.source_root, "NameNotFound"))

    def test_missing_file_suite(self):
        self.plugin_suite_register_err_test(os.path.join(self.source_root, "MissingFiles"))

    def plugin_suite_register_err_test(self, suite_source):
        try:
            self.under_test.register_suite(suite_source)
            assert False
        except Exception as e:
            print(e)
            error = self.under_test.report_suite_registration_error(suite_source)
            print(error)

    def plugin_suite_transcription_test(self, profile):
        profile_name = "TestPlugin"
        if self.under_test.is_profile(profile_name):
            self.under_test.remove_profile(profile_name)
        self.under_test.create_profile(
            name=profile_name,
            setting=profile
        )
        small_id = self.under_test.add_source(self.small_source, self.output)
        self.under_test.apply_profile_to_source(source_id=small_id, profile_name=profile_name)
        test2ab_id = self.under_test.add_source(self.test_2ab, self.output)
        self.under_test.apply_profile_to_source(source_id=test2ab_id, profile_name=profile_name)
        result = self.under_test.transcribe([small_id, test2ab_id])
        assert not result.failure
        assert not result.invalid
        assert result.success_output


if __name__ == '__main__':
    unittest.main()
