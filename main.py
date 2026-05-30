from dataclasses import dataclass, field

import arcade
import math
from arcade import Vec2


G = 3000
STEPS_PER_FRAME = 10
TRAIL_LENGTH = 3000
SOFTENING = 50


@dataclass
class Body:
    pos:   Vec2
    vel:   Vec2
    m:     float
    r:     float
    color: arcade.types.Color = arcade.color.WHITE
    acc:   Vec2       = field(init=False, default_factory=lambda: Vec2(0, 0))
    trail: list[Vec2] = field(init=False, default_factory=list)
    
    def contains(self, point: Vec2):
        return (self.pos - point).length_squared() <= math.pow(self.r, 2)

    def interact(self, other: Body):
        delta_pos = other.pos - self.pos
        
        d_sq = delta_pos.length_squared() + SOFTENING
        d = math.sqrt(d_sq)
        
        influence = delta_pos * G / (d_sq * d)

        self.acc  += influence * other.m
        other.acc -= influence *  self.m

    def update(self, dt):
        self.vel += self.acc * dt
        self.pos += self.vel * dt

        self.trail.append(self.pos)
        if len(self.trail) > TRAIL_LENGTH:
            self.trail.pop(0)

class ThreeBodySimulation(arcade.Window):
    def __init__(self, w, h):
        super().__init__(w, h, "Three-Body Problem")
        arcade.set_background_color(arcade.color.BLACK)
        
        self.mouse_pos = Vec2(0, 0)
        self.paused = False

        w2, h2 = w / 2, h / 2
        
        self.bodies = [
            Body(pos=Vec2(w2 + 300, h2), vel=Vec2(0, 100), m=10,   r=10,  color=arcade.color.RED),
            Body(pos=Vec2(w2, h2),       vel=Vec2(0, 0),   m=1000, r=60,  color=arcade.color.BLUE),
            Body(pos=Vec2(w2 - 300, h2), vel=Vec2(0, -99), m=10,   r=10,  color=arcade.color.GREEN)
        ]
        
        self.hover_hint = arcade.Text(
            "",
            0, 0,
            arcade.color.WHITE,
            font_size=14,
            width=200,
            anchor_x="left",
            anchor_y="top",
            multiline=True,
        )
        
    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pos = Vec2(x, y)
        
    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.SPACE:
            self.paused = not self.paused

    def on_draw(self):
        self.clear()
        
        for body in self.bodies:
            if body.trail:
                arcade.draw_line_strip(body.trail, body.color, 2)
                
            arcade.draw_circle_filled(*body.pos, body.r, body.color)
            
        for body in self.bodies:
            if not body.contains(self.mouse_pos):
                continue
            
            self.hover_hint.text = (
                f"Mass: {body.m}\n"
                f"Radius: {body.r}\n"
                f"Pos: ({body.pos.x:.1f}, {body.pos.y:.1f})\n"
                f"Vel: ({body.vel.x:.1f}, {body.vel.y:.1f})"
            )
            self.hover_hint.x, self.hover_hint.y = self.mouse_pos + Vec2(15, 15)
            self.hover_hint.draw()

    def on_fixed_update(self, delta_time):
        if self.paused:
            return
        
        for _ in range(STEPS_PER_FRAME):
            for body in self.bodies:
                body.acc = Vec2(0, 0)
            
            for i, b1 in enumerate(self.bodies[:-1]):
                for b2 in self.bodies[i + 1:]:
                    Body.interact(b1, b2)
                
            for body in self.bodies:
                body.update(delta_time)


if __name__ == "__main__":
    ThreeBodySimulation(1280, 720)
    arcade.run()