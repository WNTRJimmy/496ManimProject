from manim import *
from typing import Sequence

# got some help form the manim discord from user abulafia
def change_cell_content(self, row, col, new_content):
    old_content= self.get_entries((row,col))
    new_content = Paragraph(new_content, font_size=old_content.lines_text.font_size)
    new_content.move_to(old_content)
    old_content.become(new_content)
    return self

Table.change_cell_content = change_cell_content


class IRV1(Scene):
    def construct(self):
        original_list = [["20", "D", "B", "A", "C"],["10", "C", "A", "B", "D"],["23", "B", "A", "D", "X"],["13", "C", "D", "A", "B"],["14", "A", "D", "C", "X"]]
        original_list.sort()
        table = Table(original_list, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})

        for i in range(len(original_list)):
            for j in range(len(original_list[i])):
                if original_list[i][j] == "X":
                    table.get_entries([i+1, j+1]).set_color(RED)

        scheme = "Instant Runoff Voting"
        name = Text(scheme, font_size=40).to_edge(UP, buff=.00001)
        underlined = Underline(name)
        self.add(name, underlined)
        self.wait()
        self.play(table.create(), run_time=3)
        self.wait()
        self.play(table.animate.scale(.75))
        self.wait(.5)
        self.play(table.animate.to_edge(LEFT))
        self.wait()

        votes_list = [["A", "0"],["B", "0"],["C", "0"], ["D", "0"]]
        first_place = Table(votes_list, line_config={"stroke_width": 2, "color": WHITE})

        self.play(table.animate.set_opacity(0), run_time=2)
        self.wait()
        self.play(first_place.create())
        self.wait()
        self.play(first_place.animate.scale(.75))
        self.wait(.5)
        self.play(first_place.animate.to_edge(RIGHT, buff=2))
        self.wait(.5)
        self.play(table.animate.set_opacity(1), run_time=2)
        self.wait(.5)


        d = {"C": 2, "A": 0, "B": 1, "D":3}
        v = {"C": 0, "A": 0, "B": 0, "D":0}

        col = table.get_columns()[1]
        self.play(Circumscribe(col), run_time=5)

        for i in range(len(original_list)):
            seq = [i+1, 2]

            shape = table.get_cell(seq)
            self.play(Indicate(shape))
            self.add(shape)
            self.wait()
            val = original_list[i][1]
            # print(val, d[val])
            to_add = original_list[i][0]
            # current_val = votes_list[d[val]][1]
            v[val] = v[val] + int(to_add)

            self.play(first_place.animate.change_cell_content(d[val]+1, 2, str(v[val])))
            self.play(table.get_cell(seq).animate.set_color(WHITE))
            # self.remove(table.get_cell(seq))
            # self.play(FadeOut(shape))
            # self.play(table.get_cell(seq).animate.set_color(WHITE))
        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])


        for i in range(len(original_list)):
            for j in range(len(original_list[i])):
                if original_list[i][j] == "A":
                    # print(original_list[i][j], i, j)
                    seq = [i+1, j+1]
                    shape = table.get_cell(seq)
                    self.add(shape)
                    self.play(shape.animate.set_color(RED))
                    original_list[i][j] = "X"
                    
        self.play(table.animate.change_cell_content(1, 3, "X").change_cell_content(2,4,"X").change_cell_content(3, 2, "X").change_cell_content(4,4, "X").change_cell_content(5,3,"X"))
        self.wait()
        self.play(table.get_entries([1, 3]).animate.set_color(RED), table.get_entries([2, 4]).animate.set_color(RED),table.get_entries([3,2]).animate.set_color(RED),table.get_entries([4,4]).animate.set_color(RED),table.get_entries([5,3]).animate.set_color(RED), run_time=2)
        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])

        self.play(Circumscribe(first_place.get_rows()[0]), run_time=2)

        self.play(Uncreate(first_place))

        votes_list = [["B", str(v["B"])],["C", str(v["C"])], ["D", str(v["D"])]]
        first_place = Table(votes_list, line_config={"stroke_width": 2, "color": WHITE})
        
        first_place.scale(.75)
        first_place.to_edge(RIGHT, buff=2)

        self.play(first_place.create())
        self.wait()

        del v["A"]
        d = {"C": 1,"B": 0, "D":2}

        row = table.get_rows()[2]
        self.play(Circumscribe(row), run_time=5)


        seq = [3, 3]
        shape = table.get_cell(seq)
        self.play(Indicate(shape))
        self.add(shape)
        self.wait()
        val = original_list[2][2]
        # print(val, d[val])
        to_add = original_list[2][0]
        # current_val = votes_list[d[val]][1]
        v[val] = v[val] + int(to_add)

        self.play(first_place.animate.change_cell_content(d[val]+1, 2, str(v[val])))
        self.play(table.get_cell(seq).animate.set_color(WHITE))

        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])

        self.play(Circumscribe(first_place.get_rows()[:2]), run_time=4)

        self.play(first_place.get_entries([1, 1]).animate.set_color(RED), first_place.get_entries([1, 2]).animate.set_color(RED),first_place.get_entries([2,1]).animate.set_color(RED),first_place.get_entries([2,2]).animate.set_color(RED), run_time=2)

        self.wait()
