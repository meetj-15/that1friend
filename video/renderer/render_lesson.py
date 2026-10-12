import json
import subprocess
from pathlib import Path

from manim import *


ROOT = Path(__file__).resolve().parents[2]
SCENE_FILE = ROOT / "scenes" / "example_lesson.json"


class LessonScene(Scene):
    def construct(self):
        data = json.loads(SCENE_FILE.read_text(encoding="utf-8"))

        for item in data["scenes"]:
            kind = item["type"]

            if kind == "title":
                obj = Text(item["text"], font_size=52)
            elif kind == "paragraph":
                obj = Paragraph(item["text"], font_size=28, alignment="center")
            elif kind == "equation":
                obj = MathTex(item["latex"], font_size=48)
            elif kind == "diagram":
                values = item["values"]
                groups = VGroup(*[
                    Square(side_length=0.8).add(Text(str(value), font_size=24))
                    for value in values
                ]).arrange(RIGHT, buff=0.08)
                idx = int(item.get("highlight_index", -1))
                if 0 <= idx < len(values):
                    groups[idx].set_stroke(width=6)
                obj = groups
            else:
                continue

            self.play(FadeIn(obj))
            self.wait(2)
            self.play(FadeOut(obj))


if __name__ == "__main__":
    pass
# From video/renderer
manim -pqh render_lesson.py LessonScene

# If the render succeeds, inspect the MP4 before automating it.
