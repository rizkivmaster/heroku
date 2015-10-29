# import shutil
# shutil.copy('app/meloentjoer/config/config-TEST.json', '/var/meloentjoer/config/config-TEST.json')
config_file = open('/var/meloentjoer/config/config-TEST.json', 'r').readline()

print(config_file)

from app.MeloentjoerApp import MeloentjoerApp

if __name__ == "__main__":
    meloentjoer_app = MeloentjoerApp()
    meloentjoer_app.run()
