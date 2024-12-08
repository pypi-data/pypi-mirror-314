from quick_doc_py.main import worker
from quick_doc_py.config import LANGUAGE_TYPE, GPT_MODELS
from quick_doc_py.providers_test import provider_test
import argparse


class AutoDock:
    def __init__(self, 
                name_project: str,
                ignore: list[str],
                root_dir: str,
                languages: list[str],
                with_git: bool = True,
                gpt_version: str = "gpt-3.5-turbo",
                provider: str = "DarkAI",
                general_prompt: str = "",
                default_prompt: str = ""
                ):
        print(ignore)
        
        self.data = ['--name_project', name_project, 
                     '--ignore', str(ignore), 
                     "--root_dir", root_dir, 
                     "--languages", str(languages),
                     "--with_git", "True",
                     "--gpt_version", gpt_version,
                     "--provider", provider,
                     "--general_prompt", general_prompt,
                     "--default_prompt", default_prompt
                     ]

    def gen_doc(self):


        parser = argparse.ArgumentParser(description="")
        parser.add_argument("--name_project", type=str, help="name of project", required=True)
        parser.add_argument("--root_dir", type=str, help="root dir", required=True)
        parser.add_argument("--ignore", type=str, help="ignor files", required=True)
        parser.add_argument("--languages", type=str, help="language", required=True)

        parser.add_argument("--gpt_version", type=str, help="gpt version", required=False)
        parser.add_argument("--provider", type=str, help="provider", required=False)

        parser.add_argument("--general_prompt", type=str, help="general prompt", required=False)
        parser.add_argument("--default_prompt", type=str, help="default prompt", required=False)

        parser.add_argument("--with_git", type=bool, help="Is git used", required=False)


        data = parser.parse_args(self.data)


        w = worker(data)[0]
        w.save_dock(w.answer_handler)


class DataHandler:
    def __init__(self):
        pass

    def get_active_providers(self, gpt_version: str):
        providers = provider_test(gpt_version)
        return providers
    
    def support_languages(self):
        return list(LANGUAGE_TYPE.keys())

    def support_versions(self):
        return GPT_MODELS

if __name__ == "__main__":
    DataHandler().get_active_providers("gpt-3.5-turbo")
    root_dir = "C:/Users/sinic/Python_Project/Quick-doc-py UI/"
    name = "Test Project UI"
    ignore = [".venv"]
    languages = ["en"]

    AutoDock(name_project=name, root_dir=root_dir, ignore=ignore, languages=languages).gen_doc()


