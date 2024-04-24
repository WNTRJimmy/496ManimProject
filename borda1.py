from manim import *
from typing import Sequence
import random
import os
import argparse
import itertools
# from manimlib.imports import *


# got some help form the manim discord from user abulafia
def change_cell_content(self, row, col, new_content, font_size_for_table: float):
    old_content= self.get_entries((row,col))
    new_content = Paragraph(new_content, font_size=font_size_for_table)
    new_content.move_to(old_content)
    old_content.become(new_content)
    return self

Table.change_cell_content = change_cell_content

def dict_to_vals(self, d):
    l = list(d.keys())
    ret = []
    for item in l:
        ret.append(d[item])
    return ret

def max_of_dict(self, d):
    l = dict_to_vals(self, d)
    maximum = max(l)
    items_with_max = []
    for k,v in d.items():
        if v == maximum:
            items_with_max.append(k)
    return items_with_max


def generate_max_unique_rankings(
    max_unique_rankings, min_ranking_length, max_ranking_length, candidates
):
    rankings = []
    while len(rankings) < max_unique_rankings:
        new_rank = generate_random_ranking(
            random.randint(min_ranking_length, max_ranking_length), candidates
        )
        if new_rank not in rankings:
            rankings.append([0] + new_rank)

    return rankings


def distribute_votes(rankings, num_voters):
    for i in range(num_voters):
        # give all rankings at least one vote
        # if i < len(rankings):
        #     rankings[i][1] += 1
        # else:
        rankings[random.randint(0, len(rankings) - 1)][0] += 1

def generate_random_ranking(length, candidates):
    # sample is used to support using the candidates having actual names feature, which was later disabled.
    if len(candidates) == length:
        result = random.sample(candidates, length)
    else:
        result = random.sample(candidates, length)

    return result

def change_int_to_str(ranks):
    for i in range(len(ranks)):
        ranks[i][0] = str(ranks[i][0])
    return ranks

def fill_out(ranks, candidates):
    for i in range(len(ranks)):
        if(len(ranks[i]) < candidates+1):
            print(ranks[i], "TOADD  ", (["X"] * (candidates+1 - len(ranks[i]))))
            ranks[i] = ranks[i] + (["X"] * (candidates+1 - len(ranks[i])))
    return ranks

def init_dicts(candidates, old_v=None):
    v = dict()
    d = dict()
    i = 0
    for candidate in candidates:
        if(old_v is None):
            v[candidate] = 0
        else:
            v[candidate] = old_v[candidate]
        d[candidate] = i
        i+=1
    return v, d, [0] * len(candidates)

def convert_dict_to_votes_list(d):
    l = []
    for k,v in d.items():
        l.append([k,str(v)])
    return l

def create_pairwise_empty(candidates):
    l = []
    for i in range(len(candidates)+ 1):
        row = []
        for j in range(len(candidates)+ 1):
            if(i == j):
                row.append("X")
            else:
                row.append("0")
        l.append(row)
    
    for i in range(len(candidates)+ 1):
        if(i != 0):
            l[0][i] = candidates[i-1]
            l[i][0] = candidates[i-1]
    

    l[0][0] = ""
    return l

class borda1(Scene):
    def construct(self):
        self.wait()

        # there is no way of adding custom command line arguments and I am not sure how to make a similar feature
        # so below I will put all of the variables so they can be edited manually to your hearts content

        # This is the total number of rankings that will be in the final animation
        number_of_rankings = 3

        # This is the minimum nimber of candidates that must be ranked on the random ballots
        minimum_len = 3

        # This is the maximum nimber of candidates that must be ranked on the random ballots
        num_candidates = 3
    
        # This is the maximum nimber of candidates that must be ranked on the random ballots by default will be num_candidates  
        maximum_len = num_candidates
        
        # This is the number of votes that will be alloted to the random ballots
        num_votes = 35

        # This is the candidate names that are possible for the random choices will be taken from A to num candidates
        candidates_possible = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M"]

        # This is the candidates list, if set then the previous variable will be ignored
        candidates = []

        """
        If you want to input your own specific election thats great but it needs to be in a certain format:

                                        Given the following election:
                                    .-------------------------------------.
                                                15, "A", "B", "C"
                                                20, "B", "C", "A" 
                                    '-------------------------------------'

                                        The required format is:
                                    .-------------------------------------.
                                             [["15", "A", "B", "C"]
                                             ["20", "B", "C", "A"]]
                                    '-------------------------------------'

        To summarize the ranks must be in the format where the count of the ballot is the first element of the 
        ranking and it needs to be a string. Yes it NEEDS to be a string. If you want you can use the change_int_to_str function
        on your 2-D list and that function will do it for you. Also not shown above non-complete ballots are problamatic for the 
        way that the manim table function works. You need to fill out all of the non complete ballots like: 

        Assuming that the candidates are "A", "B", "C" and given the ballot ["5", "A", "B"]

        You should convert the ballot to -> ["5", "A", "B", "X"]

        Where the X is just a placeholder that fills the slot, I call that function on the candidate list so you need not worry about doing that yourself.


        """
        results = []

        # if(candidates == []):
        #     candidates = candidates_possible[0:num_candidates]
        # ranks = generate_max_unique_rankings(number_of_rankings, minimum_len, maximum_len, candidates)
        # distribute_votes(ranks, num_votes)
        # ranks = change_int_to_str(ranks)
        # ranks = fill_out(ranks, num_candidates)
        ranks = [["10","A", "B", "C"],["13","B", "C", "A"],["12","C", "B", "A"]]
        ranks2 = [["10","A", "B", "C"],["13","B", "C", "A"],["12","C", "B", "A"]]
        candidates = candidates_possible[0:num_candidates]

        # SCHEME BORDA WHERE POINTS ARE GIVEN AS ["A", "B", "C"] A would get 3 and B 2 and C 1 if you were left off the ballot 0 points
        votes = ranks
        table = Table(votes, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})
        table.scale(.75)
        for i in range(len(votes)):
            for j in range(len(votes[i])):
                if votes[i][j] == "X":
                    table.get_entries([i+1, j+1]).set_color(RED)


        scheme = "Borda Count"
        name = Text(scheme, font_size=40).to_edge(UP, buff=.00001)
        underlined = Underline(name)
        self.add(name, underlined)
        self.wait()
        self.play(Create(table))
        self.wait()
        self.play(table.animate.scale(.6))
        self.wait(.5)
        self.play(table.animate.to_edge(LEFT))
        self.wait()

        chart_y = num_votes * num_candidates
        chart_y_increment = chart_y // 10

        ret = init_dicts(candidates)
        v = ret[0]
        d = ret[1]
        value = ret[2]

        chart0 = BarChart(
            values=value,
            y_range=[0, chart_y, chart_y_increment],
            bar_names=candidates,
            y_length=8,
            x_length=8,
            bar_width = 0.5,
            x_axis_config={"font_size": 36},
            bar_colors=[BLUE, BLUE, BLUE, BLUE]
        )

        self.add(chart0)

        chart0.scale(.7)
        chart0.to_edge(RIGHT)
        self.play(Create(chart0))
        self.wait(3)



        for i in range(len(votes)):
            # surrect2 = SurroundingRectangle(table.get_rows()[i])
            # self.play(Create(surrect2), run_time=2)
            # self.wait(3)

            # self.play(Uncreate(surrect2), run_time=2)
            # self.wait(3)
            for j in range(1, len(votes[i])):
                seq = [i+1, j+1]
                self.play(table.get_cell(seq).animate.set_color(RED))
                self.wait()
                val = votes[i][j]
                if(val == "X"):
                    continue
                # print(val, d[val])
                to_add = (len(votes[i]) - j) * int(votes[i][0])
                # current_val = votes_list[d[val]][1]
                v[val] = v[val] + to_add

                to_change = dict_to_vals(self, v)

                max_bars = max_of_dict(self, v)
                colors = []
                for item in v.keys():
                    if item in max_bars:
                        colors.append(RED)
                    else:
                        colors.append(BLUE)

                new_chart = BarChart(
                    values=to_change,
                    y_range=[0, chart_y, chart_y_increment],
                    bar_names=candidates,
                    y_length=8,
                    x_length=8,
                    bar_width = 0.5,
                    x_axis_config={"font_size": 36},
                    bar_colors=colors
                )
                new_chart = new_chart.scale(.7)
                new_chart.to_edge(RIGHT)
                self.play(ReplacementTransform(chart0, new_chart, run_time = 2))
                chart0 = new_chart
            labels = new_chart.get_bar_labels(font_size=48)
            self.play(Create(labels))
            self.wait()
            if(i != len(votes)-1):
                self.play(Uncreate(labels))
            self.wait(3)
        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])
        self.wait(2)

        maximum = max(v.values())
        count = 0
        winner = None
        for k, val in v.items():
            if(val == maximum):
                count += 1
                winner = k
        if(count == 1):
            results.append(["Borda", winner])
        else:
            results.append(["Borda", "Tie"])


        # SCHEME BORDA END
        
        

        # COPELANDS METHOD
        self.clear()
        print(ranks, candidates)
        table_copelands = Table(ranks, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})

        scheme = "Copelands Method"
        name = Text(scheme, font_size=40).to_edge(UP, buff=.00001)
        underlined = Underline(name)
        self.add(name, underlined)
        self.wait()
        table_copelands.scale(.65)
        table_copelands.to_edge(LEFT)
        self.play(table_copelands.create(), run_time=3)
        self.wait()

        pairwise = create_pairwise_empty(candidates)
        print(pairwise)
        pairwise_table = Table(pairwise, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})
        pairwise_table.scale(.65)
        pairwise_table.to_edge(RIGHT)
        # for i in range(len(pairwise)):
        #     for j in range(len(pairwise[i])):
        #         if pairwise[i][j] == "X":
        #             pairwise_table.get_entries([i+1, j]).set_color(RED)

        self.play(pairwise_table.create(), run_time=3)
        self.wait()

        ret = init_dicts(candidates)
        d = ret[1]
        v = ret[0]
        print(d)
        font_size_for_table = pairwise_table.get_entries([4,3]).lines_text.font_size - 8
        for i in range(len(ranks)):
            for j in range(1, len(ranks[i])):
                self.play(Indicate(table_copelands.get_cell([i+1, j+1])))
                self.wait()
                if(j != len(ranks[i])-1):
                    self.play(Circumscribe(table_copelands.get_rows()[i][j+1:]))
                    to_increment = ranks[i][j+1:]
                    for item in to_increment:
                        pairwise[d[ranks[i][j]]+1][d[item]+1] = str(int(pairwise[d[ranks[i][j]]+1][d[item]+1]) + int(ranks[i][0]))
                        self.play(pairwise_table.animate.change_cell_content(d[ranks[i][j]]+2, d[item]+1, str(int(pairwise[d[ranks[i][j]]+1][d[item]+1])), font_size_for_table))

        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])
        self.play(Uncreate(table_copelands))

        self.wait()
        self.play(pairwise_table.animate.to_edge(LEFT, buff=4.8))
        self.wait()
        self.play(pairwise_table.animate.scale(1.3))
        self.wait()
        font_size_for_table = pairwise_table.get_entries([4,3]).lines_text.font_size - 8
        c = range(1, num_candidates+1)
        cart = itertools.product(c, c)
        cart_product = list(cart)

        while len(cart_product) > 0:
            position: tuple[int, int] = cart_product.pop(0)
            if position[0] == position[1]:
                continue
            val_at_position: int = int(pairwise[position[0]][position[1]])
            oppsite_value: int = int(pairwise[position[1]][position[0]])

            self.play(Circumscribe(pairwise_table.get_entries([position[0]+1, position[1]])), Circumscribe(pairwise_table.get_entries([position[1]+1, position[0]])), run_time=2)
            self.wait()
            if val_at_position > oppsite_value:
                pairwise[position[0]][position[1]] = str(1)
                pairwise[position[1]][position[0]] = str(0)
                self.play(pairwise_table.animate.change_cell_content(position[0]+1, position[1], pairwise[position[0]][position[1]], font_size_for_table).change_cell_content(position[1]+1, position[0], pairwise[position[1]][position[0]], font_size_for_table))
                to_remove: tuple[int, int] = (position[1], position[0])
                cart_product.remove(to_remove)
            elif val_at_position < oppsite_value:
                pairwise[position[0]][position[1]] = str(0)
                pairwise[position[1]][position[0]] = str(1)
                self.play(pairwise_table.animate.change_cell_content(position[0]+1, position[1], pairwise[position[0]][position[1]], font_size_for_table).change_cell_content(position[1]+1, position[0], pairwise[position[1]][position[0]], font_size_for_table))
                to_remove = (position[1], position[0])
                cart_product.remove(to_remove)
            else:
                pairwise[position[0]][position[1]] = str(.5)
                pairwise[position[1]][position[0]] = str(.5)
                self.play(pairwise_table.animate.change_cell_content(position[0]+1, position[1], pairwise[position[0]][position[1]], font_size_for_table).change_cell_content(position[1]+1, position[0], pairwise[position[1]][position[0]], font_size_for_table))
                to_remove = (position[1], position[0])
                cart_product.remove(to_remove)
            self.wait()


        for i in range(len(pairwise)):
            for j in range(len(pairwise[i])):
                if(i > 0 and j > 0 and i != j):
                    if int(pairwise[i][j]) > 0:
                        v[pairwise[i][0]] = v[pairwise[i][0]] + int(pairwise[i][j])
            
        maximum = max(v.values())
        count = 0
        winner = None
        winners = []
        for k, val in v.items():
            if val == maximum:
                count += 1
                winner = k
                winners.append(k)
        if count == 1:
            results.append(["Copeland", winner])
            self.play(pairwise_table.get_rows()[d[winner]+1].animate.set_color(RED))
            self.wait(2)
            if(v[winner] == num_candidates-1):
                results.append(["Condorcet", winner])
            else:
                results.append(["Condorcet", "None"])
        else:
            for k in winners:
                self.play(Circumscribe(pairwise_table.get_rows()[d[k]+1]), run_time=2)
            results.append(["Copeland", "Tie"])
        

# SCHEME IRV if over 50% margin that candidate instantly wins

        self.clear()
        # ranks = [['23', 'B', 'C', 'A'], ['19', 'C', 'A', 'B'], ['18', 'A', 'C', 'B'], ['22', 'C', 'B', 'A'], ['18', 'A', 'B', 'C']]
        IRV_ranks = ranks.copy()
        IRV_cands = candidates.copy()
        table1 = Table(IRV_ranks, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})

        for i in range(len(IRV_ranks)):
            for j in range(len(IRV_ranks[i])):
                if IRV_ranks[i][j] == "X":
                    table1.get_entries([i+1, j+1]).set_color(RED)

        scheme = "Instant Runoff Voting"
        name = Text(scheme, font_size=40).to_edge(UP, buff=.00001)
        underlined = Underline(name)
        self.add(name, underlined)
        self.wait()
        table1.scale(.65)
        table1.to_edge(LEFT)
        self.play(table1.create(), run_time=3)
        self.wait()

        votes_list = []
        for i in range(len(IRV_cands)):
            votes_list.append([IRV_cands[i], "0"])

        first_place = Table(votes_list, line_config={"stroke_width": 2, "color": WHITE})
        font_size_for_table = first_place.get_entries([1,1]).lines_text.font_size - 8
        print(font_size_for_table, type(font_size_for_table))


        first_place.scale(.75)
        first_place.to_edge(RIGHT, buff=2)
        self.play(first_place.create())
        self.wait()

        ret = init_dicts(IRV_cands)
        v = ret[0]
        d = ret[1]

        col = table1.get_columns()[1]
        self.play(Circumscribe(col), run_time=5)

        for i in range(len(IRV_ranks)):
            seq = [i+1, 2]

            shape = table1.get_cell(seq)
            self.play(Indicate(shape))
            self.add(shape)
            self.wait()
            val = IRV_ranks[i][1]

            to_add = IRV_ranks[i][0]

            v[val] = v[val] + int(to_add)

            self.play(first_place.animate.change_cell_content(d[val]+1, 2, str(v[val]), font_size_for_table))
            self.play(table1.get_cell(seq).animate.set_color(WHITE))
            # self.remove(table.get_cell(seq))
            # self.play(FadeOut(shape))
            # self.play(table.get_cell(seq).animate.set_color(WHITE))
        self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])

        winner = None
        iteration = 1
        while(True):
            for k, val  in v.items():
                if int(val) / num_votes > .5:
                    winner = k

            if(winner is not None):
                self.play(Circumscribe(first_place.get_rows()[d[winner]]), run_time=4)
                self.play(first_place.get_rows()[d[winner]].animate.set_color(RED))
                break

            cands_with_min = []
            min_val = min(v.values())
            print(v, min_val)
            for k, val in v.items():
                if int(val) == min_val:
                    cands_with_min.append(k)
            if(len(cands_with_min) > 1):
                for can in cands_with_min:
                    self.play(Circumscribe(first_place.get_rows()[d[can]]), run_time=4)
                new_first_place = first_place
                for can in cands_with_min:
                    new_first_place.get_rows()[d[can]].set_color(RED)
                    # self.play(Uncreate(first_place))
                self.play(ReplacementTransform(new_first_place, first_place, run_time=3), run_time=3)
                first_place = new_first_place
                results.append(["IRV", "Tie"])
                break
            
            to_eliminate = cands_with_min[0]
            IRV_cands.remove(to_eliminate)

            ret = init_dicts(IRV_cands, v)
            v = ret[0]
            d = ret[1]

            for i in range(len(IRV_ranks)):
                for j in range(len(IRV_ranks[i])):
                    if IRV_ranks[i][j] == to_eliminate:
                        # print(original_list[i][j], i, j)
                        seq = [i+1, j+1]
                        shape = table1.get_cell(seq)
                        self.add(shape)
                        self.play(shape.animate.set_color(RED))
                        IRV_ranks[i][j] = "X"
            
            votes_list1 = convert_dict_to_votes_list(v)
            new_first_place = Table(votes_list1, line_config={"stroke_width": 2, "color": WHITE})
            new_first_place.scale(.75)
            new_first_place.to_edge(RIGHT, buff=2)
 

            self.wait()
            new_table1 = table1
            for i in range(len(IRV_ranks)):
                for j in range(len(IRV_ranks[i])):
                    if IRV_ranks[i][j] == "X":
                        self.play(table1.animate.change_cell_content(i+1, j+1, "X", font_size_for_table))
                        new_table1.get_entries([i+1,j+1]).set_color(RED)


            self.play(ReplacementTransform(new_table1, table1),ReplacementTransform(first_place, new_first_place), run_time=3)
            first_place = new_first_place
            table1 = new_table1
            
            self.wait()
            table1 = new_table1
            self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])

            for i in range(len(IRV_ranks)):
                if IRV_ranks[i][iteration] == "X":
                    shape = table1.get_cell([i+1, iteration+2])
                    self.play(Indicate(shape))
                    self.add(shape)
                    self.wait(2)
                    val = IRV_ranks[i][iteration+1]
                    print(f"VAL SHOUD BE C == {val}")

                    to_add = IRV_ranks[i][0]
                    print(v)
                    v[val] = v[val] + int(to_add)
                    print(v)
                    self.play(first_place.animate.change_cell_content(d[val]+1, 2, str(v[val]), font_size_for_table))
                    self.play(table1.get_cell([i+1, iteration+2]).animate.set_color(WHITE))
                    
            self.play(*[FadeOut(mob) for mob in self.mobjects if type(mob) == Polygon])
            iteration+=1
        results.append(["IRV", winner])

        # # SCHEME IRV END
        self.clear()



        table_results = Table(ranks2, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})

        scheme = "Results"
        name = Text(scheme, font_size=40).to_edge(UP, buff=.00001)
        underlined = Underline(name)
        self.add(name, underlined)
        self.wait()
        table_results.scale(.65)
        table_results.to_edge(LEFT)
        self.play(table_results.create(), run_time=3)
        self.wait()

        table_results1 = Table(results, include_outer_lines=True, line_config={"stroke_width": 2, "color": WHITE})
        self.wait()
        table_results1.scale(.65)
        table_results1.to_edge(RIGHT)
        self.play(table_results1.create(), run_time=3)
        self.wait(4)




            











