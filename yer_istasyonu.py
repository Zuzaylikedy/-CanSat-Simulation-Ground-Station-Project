import math
import random
import tkinter as tk

import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

SIMULATION_MODE = True


class CanSatGroundStation:
    def __init__(self, root):
        self.root = root
        self.root.title("CanSat Ground Station & Telemetry Interface")
        self.root.geometry("1000x650")
        self.root.configure(bg="#1e1e2e")

        self.packet_no = 0
        self.altitude = 543.0  # Our OpenRocket apex
        self.temperature = 24.5
        self.compass_angle = 0.0

        self.time_data = []
        self.alt_data = []

        self._setup_ui()
        self.update_telemetry()

    def _setup_ui(self):
        left_frame = tk.Frame(self.root, bg="#1e1e2e", padx=10, pady=10)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False)

        lbl_compass = tk.Label(
            left_frame,
            text="Compass (Direction)",
            fg="#cdd6f4",
            bg="#1e1e2e",
            font=("Helvetica", 14, "bold"),
        )
        lbl_compass.pack(pady=5)

        self.compass_canvas = tk.Canvas(
            left_frame, width=220, height=220, bg="#181825", highlightthickness=0
        )
        self.compass_canvas.pack(pady=10)

        self.info_frame = tk.Frame(
            left_frame, bg="#313244", padx=15, pady=15, relief=tk.RIDGE, bd=2
        )
        self.info_frame.pack(fill=tk.X, pady=10)

        self.lbl_packet = tk.Label(
            self.info_frame,
            text="Packet No: 0",
            fg="#a6e3a1",
            bg="#313244",
            font=("Consolas", 12, "bold"),
        )
        self.lbl_packet.pack(anchor="w", pady=2)

        self.lbl_altitude = tk.Label(
            self.info_frame,
            text="Altitude: 543.0 m",
            fg="#89b4fa",
            bg="#313244",
            font=("Consolas", 12, "bold"),
        )
        self.lbl_altitude.pack(anchor="w", pady=2)

        self.lbl_temperature = tk.Label(
            self.info_frame,
            text="Temperature: 24.5 °C",
            fg="#fab387",
            bg="#313244",
            font=("Consolas", 12, "bold"),
        )
        self.lbl_temperature.pack(anchor="w", pady=2)

        self.lbl_angle = tk.Label(
            self.info_frame,
            text="Compass Angle: 0.0°",
            fg="#f9e2af",
            bg="#313244",
            font=("Consolas", 12, "bold"),
        )
        self.lbl_angle.pack(anchor="w", pady=2)

        right_frame = tk.Frame(self.root, bg="#1e1e2e", padx=10, pady=10)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6, 4), dpi=100, facecolor="#181825")
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor("#1e1e2e")
        self.ax.tick_params(colors="#cdd6f4")
        self.ax.set_title(
            "Live Altitude / Descent Graph", color="#cdd6f4", fontsize=12, fontweight="bold"
        )
        self.ax.set_xlabel("Time (s)", color="#cdd6f4")
        self.ax.set_ylabel("Altitude (m)", color="#cdd6f4")
        self.ax.grid(True, color="#45475a", linestyle="--")

        (self.line,) = self.ax.plot([], [], color="#89b4fa", linewidth=2)

        self.canvas = FigureCanvasTkAgg(self.fig, master=right_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_compass(self, angle_deg):
        """Draws the compass dial and needle."""
        self.compass_canvas.delete("all")
        cx, cy, r = 110, 110, 90

        self.compass_canvas.create_oval(
            cx - r, cy - r, cx + r, cy + r, outline="#585b70", width=3
        )

        self.compass_canvas.create_text(
            cx, cy - r + 15, text="N", fill="#f38ba8", font=("Helvetica", 11, "bold")
        )
        self.compass_canvas.create_text(
            cx, cy + r - 15, text="S", fill="#cdd6f4", font=("Helvetica", 10)
        )
        self.compass_canvas.create_text(
            cx + r - 15, cy, text="E", fill="#cdd6f4", font=("Helvetica", 10)
        )
        self.compass_canvas.create_text(
            cx - r + 15, cy, text="W", fill="#cdd6f4", font=("Helvetica", 10)
        )

        rad = math.radians(angle_deg - 90)
        tip_x = cx + (r - 25) * math.cos(rad)
        tip_y = cy + (r - 25) * math.sin(rad)

        self.compass_canvas.create_line(
            cx, cy, tip_x, tip_y, fill="#f38ba8", width=4, arrow=tk.LAST
        )
        self.compass_canvas.create_oval(cx - 5, cy - 5, cx + 5, cy + 5, fill="#cdd6f4")

    def update_telemetry(self):
        """Receives, processes telemetry data, and updates the interface."""
        if SIMULATION_MODE:
            self.packet_no += 1

            if self.altitude > 0:
                turbulence = random.uniform(-0.3, 0.3)
                self.altitude -= 1.0 + turbulence
            else:
                self.altitude = 0

            drift = random.uniform(-4.0, 6.0)
            self.compass_angle = (self.compass_angle + drift) % 360.0
            self.temperature = 24.5 + random.uniform(-0.1, 0.1)

        self.lbl_packet.config(text=f"Packet No: {self.packet_no}")
        self.lbl_altitude.config(text=f"Altitude: {self.altitude:.1f} m")
        self.lbl_temperature.config(text=f"Temperature: {self.temperature:.1f} °C")
        self.lbl_angle.config(text=f"Compass Angle: {self.compass_angle:.1f}°")

        self.draw_compass(self.compass_angle)

        self.time_data.append(self.packet_no * 0.1)
        self.alt_data.append(self.altitude)

        if len(self.time_data) > 200:
            self.time_data.pop(0)
            self.alt_data.pop(0)

        self.line.set_data(self.time_data, self.alt_data)
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw_idle()

        self.root.after(100, self.update_telemetry)


if __name__ == "__main__":
    root = tk.Tk()
    app = CanSatGroundStation(root)
    root.mainloop()
