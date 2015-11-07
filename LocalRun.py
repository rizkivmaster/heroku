# import shutil
# shutil.copy('app/meloentjoer/config/config-TEST.json', '/var/meloentjoer/config/config-TEST.json')
config_file = open('/var/meloentjoer/config/config-TEST.json', 'r').readline()

print(config_file)

# from app.meloentjoer.test.test_component import MeloentjoerApp
from app.meloentjoer.main_controller import meloentjoer_app
if __name__ == "__main__":
    meloentjoer_app.run()
