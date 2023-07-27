"""
Tablet Mode Driver
"""
import subprocess
from lib.event.plugins.shell.observable import ShellObservableConsumer
from lib.event.observer import Observer

class OrientationListener(Observer):
    """OrientationListener class"""

    def __init__(self, observable, keyboard_name='Asus Keyboard'):
        super().__init__(observable)
        self.keyboards = self.get_keyboards(keyboard_name)
        self.first_run = True
        self.listen(self.observable.command, self.fetch)

    def fetch(self, line):
        """Update method"""
        if 'normal' in line:
            self.first_run = False
            self.reset_tablet_mode()
        else:
            if not self.first_run:
                self.set_tablet_mode()

    def reset_tablet_mode(self):
        """Reset tablet mode"""
        self.set_touchpad(True)
        self.set_screen_keyboard(False)
        self.set_keyboard(True)
        print('Normal')

    def set_tablet_mode(self):
        """Set tablet mode"""
        self.set_touchpad(False)
        self.set_screen_keyboard(True)
        self.set_keyboard(False)
        print('Not Normal')

    def set_touchpad(self, state):
        """Set touchpad state"""
        state_literal = 'enabled' if state else 'disabled'
        command = 'gsettings set org.gnome.desktop.peripherals.touchpad send-events ' \
            f'{state_literal}'
        self.run_command(command)

    def set_screen_keyboard(self, state):
        """Set screen keyboard state"""
        state_literal = 'true' if state else 'false'
        command = 'gsettings set org.gnome.desktop.a11y.applications screen-keyboard-enabled ' \
            f'{state_literal}'
        self.run_command(command)

    def set_keyboard(self, state):
        """Set keyboard state"""
        for keyboard in self.keyboards:
            if state:
                command = f'xinput reattach {keyboard["id"]} {keyboard["master_id"]}'
            else:
                command = f'xinput float {keyboard["id"]}'
            self.run_command(command)

    def run_command(self, command):
        """Run command"""
        cmd = ['/usr/bin/bash', '-c', command]
        subprocess.Popen(cmd)

    def get_keyboards(self, keyboard_name):
        """Get keyboards"""
        found_keyboards = []
        command = 'xinput list'
        cmd = ['/usr/bin/bash', '-c', command]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        output, _ = process.communicate()
        keyboards = output.decode('utf-8').split('\n')
        for keyboard in keyboards:
            # get the id and the master id of the keyboard anmed keyboard_name
            if keyboard_name in keyboard:
                if 'slave  keyboard' not in keyboard:
                    continue
                keyboard_id = keyboard.split('id=')[1].split('\t')[0]
                keyboard_master_id = keyboard.split('slave  keyboard (')[1].split(')')[0]
                found_keyboards.append({
                    'id': keyboard_id,
                    'master_id': keyboard_master_id
                })
        return found_keyboards

def main():
    """Main function"""
    observable = ShellObservableConsumer('monitor-sensor --accel')
    OrientationListener(observable, 'Asus Keyboard')
    observable.consume()

if __name__ == '__main__':
    main()
