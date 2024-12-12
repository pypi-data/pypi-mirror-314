import streamlit as st
import json
import os

def fix_name(name):
    return name.replace(":", "").replace(" ", "_")

class SessionStateManager:
    def __init__(self, instance_id, main_key, main_values, main_default):
        """
        1. get the key from default config
        2. if the key-value is valid 
           a. get the secondary config ss values based on key-value
           b. if not valid, set the key default
        """
        instance_id = instance_id if instance_id is not None else "DEFAULT"
        self.main_key = main_key
        self.main_default = main_default
        self.config_dir = f"session_manager_configs/{fix_name(instance_id)}"

        os.makedirs(self.config_dir, exist_ok=True)

        default_config = f"{self.config_dir}/default.json"
        if os.path.exists(default_config):
            try:
                cached_settings = json.loads(open(default_config).read())
            except Exception:
                cached_settings = {}
        else:
            cached_settings = {}

        if self.main_key in cached_settings:
            if cached_settings[self.main_key] not in main_values:
                # Invalid setting, return to default
                if self.main_key in st.session_state and st.session_state[self.main_key] == main_default:
                    pass
                else:
                    # Only set if it has changed:
                    st.session_state[self.main_key] = main_default
            else:
                # Restore from config:
                if self.main_key in st.session_state and st.session_state[self.main_key] == cached_settings[self.main_key]:
                    pass
                else:
                    # Only set if it has changed:
                    st.session_state[self.main_key] = cached_settings[self.main_key]


    def load(self, initial):
        # load secondary values based on main_key value
        seconday_config = f"{self.config_dir}/{fix_name(st.session_state[self.main_key])}.json"

        if os.path.exists(seconday_config):
            try:
                cached_settings = json.loads(open(seconday_config).read())
            except Exception:
                cached_settings = {}
        else:
            cached_settings = {}

        for key, value in initial.items():
            if key not in st.session_state:
                if key in cached_settings:
                    if key in st.session_state and st.session_state[key] == cached_settings[key]:
                        pass
                    else:
                        st.session_state[key] = cached_settings[key]
                else:
                    if key in st.session_state and st.session_state[key] == initial[key]:
                        pass
                    else:
                        st.session_state[key] = initial[key]

    def save_main(self, main_value):
        # First, save the main_key, main_value in default config:
        default_config = f"{self.config_dir}/default.json"
        with open(default_config, "w") as fp:
            json.dump({self.main_key: main_value}, fp)

    def save(self, keys={}):
        # save the keys in secondary config:
        if st.session_state[self.main_key] != self.main_default and keys:
            seconday_config = f"{self.config_dir}/{fix_name(st.session_state[self.main_key])}.json"
            settings = {}
            for key in keys:
                if key in st.session_state:
                    settings[key] = st.session_state[key]
            with open(seconday_config, "w") as fp:
                json.dump(settings, fp)
