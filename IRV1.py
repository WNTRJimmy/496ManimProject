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
        original_list = [["15", "A", "B", "C"],["10", "B", "A", "C"],["5", "C", "A", "B"]]
        original_list.sort()
        table = Table(original_list, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})
        scheme = "Instant Runoff Voting"
        name = Text(scheme, font_size=40).to_edge(UP, buff=.00001)
        underlined = Underline(name)
        self.add(name, underlined)
        self.wait()
        self.play(table.create())
        self.wait()
        self.play(table.animate.scale(.75))
        self.wait(.5)
        self.play(table.animate.to_edge(LEFT))
        self.wait()


        votes_list = [["A", "0"],["B", "0"],["C", "0"]]
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

        # surrect = SurroundingRectangle(table.get_columns()[1])

        # self.play(Create(surrect), run_time=2)
        # self.wait(3)
        # self.play(Uncreate(surrect), run_time=2)
        # self.wait(3)

        d = {"C": 2, "A": 0, "B": 1}
        v = {"C": 0, "A": 0, "B": 0}

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

        # for i in range(len(original_list)):
        #     surrect2 = SurroundingRectangle(table.get_rows()[i])
        #     self.play(Create(surrect2), run_time=2)
        #     self.wait(3)

        #     self.play(Uncreate(surrect2), run_time=2)
        #     self.wait(3)

        #     for j in range(1, len(original_list[i])):
        #         seq = [i+1, j+1]
        #         self.play(table.get_cell(seq).animate.set_color(RED))
        #         self.wait()
        #         val = original_list[i][j]
        #         # print(val, d[val])
        #         to_add = original_list[i][0]
        #         # current_val = votes_list[d[val]][1]
        #         v[val] = v[val] + int(to_add)

        #         self.play(first_place.animate.change_cell_content(d[val], 2, str(v[val])))
        #         self.play(table.get_cell(seq).animate.set_color(WHITE))


        for i in range(len(original_list)):
            for j in range(len(original_list[i])):
                if original_list[i][j] == "C":
                    # print(original_list[i][j], i, j)
                    seq = [i+1, j+1]
                    shape = table.get_cell(seq)
                    self.add(shape)
                    self.play(shape.animate.set_color(RED))
        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])
        self.play(FadeOut(table), FadeOut(first_place))


        original_list = [["15", "A", "B", "X"],["10", "B", "A", "X"],["5", "X", "A", "B"]]    
        original_list.sort()
        table = Table(original_list, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})
        for i in range(len(original_list)):
            for j in range(len(original_list[i])):
                if original_list[i][j] == "X":
                    table.get_entries([i+1, j+1]).set_color(RED)
        table.scale(.75)
        table.to_edge(LEFT)
        self.wait()
        self.play(table.create())


        self.wait(2)

        v1 = {"A": v["A"], "B" : v["B"]}
        del d["C"]
        

        votes_list = [["A", str(v["A"])],["B", str(v["B"])]]
        # print(votes_list)
        first_place = Table(votes_list, line_config={"stroke_width": 2, "color": WHITE})

        first_place.scale(.75)
        first_place.to_edge(RIGHT, buff=2)
        table.set_opacity(1)
        self.play(first_place.create())
        self.wait()

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

        self.wait(2)

        self.play(first_place.get_rows()[0].animate.set_color(RED))
        
        self.wait(5)
            

