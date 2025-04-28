import tkinter as tk
import typing as t

from cpusim.backend.peripherals import gpio
from cpusim.frontend.gui import base


class BugTrapSimulatorWindow(tk.Toplevel, t.Generic[base.CpuT]):
    def __init__(self, parent: tk.Tk, state: base.AppState[base.CpuT]) -> None:
        super().__init__(parent)
        self.state = state
        assert self.state.cpu.gpio is not None
        self.bug_trap_device = next(d for d in self.state.cpu.gpio._devices if isinstance(d, gpio.BugTrap))

        self.title("Bug Trap")
        self.resizable(False, False)

        self.protocol("WM_DELETE_WINDOW", lambda: None)

        trap_state_frame = tk.LabelFrame(self, text="Trap State")
        trap_state_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        self._trap_state_var = tk.StringVar(value="Open")
        self._trap_state_label = tk.Label(trap_state_frame, textvariable=self._trap_state_var, width=10, fg="green")
        self._trap_state_label.pack(padx=5, pady=5)
        self._led_state_var = tk.StringVar(value="LED Off")
        self._led_state_label = tk.Label(trap_state_frame, textvariable=self._led_state_var, width=10, fg="black")
        self._led_state_label.pack(padx=5, pady=5)

        sensor_frame = tk.LabelFrame(self, text="Sensors")
        sensor_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        self._sensor1_var, self._sensor2_var = tk.BooleanVar(value=False), tk.BooleanVar(value=False)
        tk.Checkbutton(
            sensor_frame, text="Sensor 1", variable=self._sensor1_var, command=lambda: self._set_sensor(1)
        ).pack(anchor="w", padx=5, pady=2)
        tk.Checkbutton(
            sensor_frame, text="Sensor 2", variable=self._sensor2_var, command=lambda: self._set_sensor(2)
        ).pack(anchor="w", padx=5, pady=2)

        mode_frame = tk.LabelFrame(self, text="Trap Mode")
        mode_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")
        self._mode_var = tk.BooleanVar(value=False)
        tk.Radiobutton(
            mode_frame, text="Auto", variable=self._mode_var, value=False, command=lambda: self._set_mode(False)
        ).pack(anchor="w", padx=5, pady=2)
        tk.Radiobutton(
            mode_frame, text="Manual", variable=self._mode_var, value=True, command=lambda: self._set_mode(True)
        ).pack(anchor="w", padx=5, pady=2)

        trigger_frame = tk.LabelFrame(self, text="Manual Trigger")
        trigger_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew")
        self._trigger_var = tk.BooleanVar(value=False)
        self._trigger_btn = tk.Button(
            trigger_frame, text="Fire OFF", command=self._trigger, state=tk.DISABLED, relief=tk.RAISED
        )
        self._trigger_btn.pack(padx=10, pady=10)

    def _set_sensor(self, id: t.Literal[1, 2]) -> None:
        if id == 1:
            self.bug_trap_device.sensor_1_triggered = self._sensor1_var.get()
        else:
            self.bug_trap_device.sensor_2_triggered = self._sensor2_var.get()

    def _set_mode(self, manual: bool) -> None:
        self.bug_trap_device.mode_switch_manual = manual
        if manual:
            self._trigger_btn.configure(state=tk.ACTIVE)
        else:
            self._trigger_btn.configure(text="Fire OFF")
            self._trigger_btn.configure(state=tk.DISABLED)
            self.bug_trap_device.fire_button_pressed = False

    def _trigger(self) -> None:
        if self._trigger_var.get():
            self._trigger_btn.configure(text="Fire OFF", relief=tk.RAISED)
            self.bug_trap_device.fire_button_pressed = False
        else:
            self._trigger_btn.configure(text="Fire ON", relief=tk.SUNKEN)
            self.bug_trap_device.fire_button_pressed = True

        self._trigger_var.set(self.bug_trap_device.fire_button_pressed)

    def refresh(self) -> None:
        if self.bug_trap_device.trap_closed:
            self._trap_state_var.set("Closed")
            self._trap_state_label.config(fg="red")
        else:
            self._trap_state_var.set("Open")
            self._trap_state_label.config(fg="green")

        if self.bug_trap_device.led_on:
            self._led_state_var = tk.StringVar(value="LED On")
            self._led_state_label.config(fg="red")
        else:
            self._led_state_var = tk.StringVar(value="LED Off")
            self._led_state_label.config(fg="black")
