import GeneticAlgorithm
import matplotlib.pyplot as plt
import networkx as nx
from tkinter import *
from tkinter import font
from tkinter import messagebox
from PIL import ImageTk, Image
import ast

# Example of graph as string to enter in entry in gui (take it with {})
string1 = '''
{"a": {"b": 12, "c": 10, "g": 12},
    "b": {"a": 12, "c": 8, "d": 12},
    "c": {"a": 10, "b": 8, "d": 11, "g": 9},
    "d": {"b": 12, "c": 11, "e": 11, "f": 10},
    "e": {"c": 3, "d": 11, "f": 6, "g": 7},
    "f": {"d": 10, "e": 6, "g": 9},
    "g": {"a": 12, "c": 9, "e": 7, "f": 9}}
'''
string2 = '''
{"A": {"B": 16},
    "B": {"C": 21},
    "C": {"D": 12},
    "D": {"E": 15, "B": 9},
    "E": {"D": 15, "F": 16},
    "F": {"E": 16, "A": 34, "C": 7}}
'''

graph = None
firstNode = None

def plot_fitness_evolution(num_fitness, all_fitness):
    plt.plot(range(num_fitness), all_fitness)
    plt.xlabel("Generation")
    plt.ylabel("Best Fitness")
    plt.title("Evolution of Best Fitness")
    custom_x_labels = ["Gen {}".format(i + 1) for i in range(0, num_fitness, 10)]
    plt.xticks(range(0, num_fitness, 10), custom_x_labels, rotation=45)
    plt.savefig('plot.png')
    # plt.show()

def create() :
    global graph, firstNode, graphEntry, graphlabel
    graph_str = graphEntry.get()
    graph = ast.literal_eval(graph_str)
    firstNode = list(graph.keys())[0]

    plt.clf()
    G = nx.Graph()
    for node, edges in graph.items():
        G.add_node(node)
        for edge, weight in edges.items():
            G.add_edge(node, edge, weight=weight)

    layout = nx.spring_layout(G)
    nx.draw(G, layout, with_labels=True, node_size=1000, font_size=18, font_color='#ffffff', node_color='#A5A5A5')
    edge_labels = {(u, v): d['weight'] for u, v, d in G.edges(data=True)}
    nx.draw_networkx_edge_labels(G, layout, edge_labels=edge_labels, font_size=15)

    plt.savefig('graph.png')
    image_file = "graph.png"
    image = Image.open(image_file)
    image = image.resize((300, 250))
    photo = ImageTk.PhotoImage(image)
    graphlabel.config(image=photo)
    graphlabel.image = photo

def slove():
    global graph, stoppingCriteria, generationEntry, populationEntry, crossoverEntry, mutationEntry, elitismEntry, selection, firstNode, plotlabel

    stopping_criteria_num = stoppingCriteria.get()
    num_generations_str = generationEntry.get()
    num_population_str = populationEntry.get()
    crossover_percentage_str = crossoverEntry.get()
    mutation_percentage_str = mutationEntry.get()
    elitism_percentage_str = elitismEntry.get()
    selection_num = selection.get()

    if graph == None:
        # print("Enter Graph First")
        messagebox.showinfo("Error", "Enter Graph First")
    elif stopping_criteria_num == 0:
        # print("Fill the Form Completely")
        messagebox.showinfo("Error", "Complete the Form")
    elif stopping_criteria_num == 2 and num_generations_str == "00":
        # print("Fill the Form Completely")
        messagebox.showinfo("Error", "Complete the Form")
    elif num_population_str == "00" or crossover_percentage_str == "%" or mutation_percentage_str == "%" or elitism_percentage_str == "%":
        # print("Fill the Form Completely")
        messagebox.showinfo("Error", "Complete the Form")
    elif selection_num == 0:
        # print("Fill the Form Completely")
        messagebox.showinfo("Error", "Complete the Form")
    else:
        stopping_criteria = None
        num_generations = 0
        num_population = int(num_population_str)
        crossover_percentage = int(crossover_percentage_str) / 100
        mutation_percentage = int(mutation_percentage_str) / 100
        elitism_percentage = int(elitism_percentage_str) / 100
        selection_type = None

        if stopping_criteria_num == 1:
            stopping_criteria = 'saturation'
            num_generations = 0
        else:
            stopping_criteria = 'generation'
            num_generations = int(num_generations_str)

        if selection_num == 1:
            selection_type = 'Ranking'
        else:
            selection_type = 'Tournament'


        if stopping_criteria_num == 2 and num_generations <= 0:
            # print("Enter valid values in Generations (greater than 0)")
            messagebox.showinfo("Error", "Enter valid values in Generations (greater than 0)")
        elif num_population <= 0:
            # print("Enter valid values in Population (greater than 0)")
            messagebox.showinfo("Error", "Enter valid values in Population (greater than 0)")
        elif crossover_percentage < 0 or crossover_percentage > 1:
            # print("Enter valid values in Crossover (from 0 to 100)")
            messagebox.showinfo("Error", "Enter valid values in Crossover (from 0 to 100)")
        elif mutation_percentage < 0 or mutation_percentage > 1:
            # print("Enter valid values in Mutation (from 0 to 100)")
            messagebox.showinfo("Error", "Enter valid values in Mutation (from 0 to 100)")
        elif elitism_percentage <= 0 or elitism_percentage > 1:
            # print("Enter valid values in Elitism (from 1 to 100)")
            messagebox.showinfo("Error", "Enter valid values in Elitism (from 1 to 100)")

        else:
            best_chromosome, best_fitness, all_fitness, num_fitness = GeneticAlgorithm.evolve(graph, stopping_criteria,
            num_generations, num_population, crossover_percentage, mutation_percentage,
            elitism_percentage, selection_type, firstNode)

            print("Starting from", firstNode)
            print("Best Chromosome: a ->", " -> ".join(best_chromosome), "-> a")
            print("Best Fitness:", best_fitness)
            print()

            plt.clf()

            plot_fitness_evolution(num_fitness, all_fitness)

            image_file1 = "plot.png"
            image1 = Image.open(image_file1)
            image1 = image1.resize((370, 320))
            photo1 = ImageTk.PhotoImage(image1)
            plotlabel.config(image=photo1)
            plotlabel.image = photo1

def on_entry_click(event):
    global generationEntry
    if generationEntry.get() == "00":
        generationEntry.delete(0, END)
        generationEntry.config(fg="white")

def on_entry_click1(event):
    global populationEntry
    if populationEntry.get() == "00":
        populationEntry.delete(0, END)
        populationEntry.config(fg="white")

def on_entry_click2(event):
    global crossoverEntry
    if crossoverEntry.get() == "%":
        crossoverEntry.delete(0, END)
        crossoverEntry.config(fg="white")

def on_entry_click3(event):
    global mutationEntry
    if mutationEntry.get() == "%":
        mutationEntry.delete(0, END)
        mutationEntry.config(fg="white")

def on_entry_click4(event):
    global elitismEntry
    if elitismEntry.get() == "%":
        elitismEntry.delete(0, END)
        elitismEntry.config(fg="white")

def on_focus_out(event):
    global generationEntry
    if generationEntry.get() == "":
        generationEntry.insert(0, "00")
        generationEntry.config(fg="white")

def on_focus_out1(event):
    global populationEntry
    if populationEntry.get() == "":
        populationEntry.insert(0, "00")
        populationEntry.config(fg="white")

def on_focus_out2(event):
    global crossoverEntry
    if crossoverEntry.get() == "":
        crossoverEntry.insert(0, "%")
        crossoverEntry.config(fg="white")

def on_focus_out3(event):
    global mutationEntry
    if mutationEntry.get() == "":
        mutationEntry.insert(0, "%")
        mutationEntry.config(fg="white")

def on_focus_out4(event):
    global elitismEntry
    if elitismEntry.get() == "":
        elitismEntry.insert(0, "00")
        elitismEntry.config(fg="white")

# ----------------------------------------------------------------------------------------------------------------------
# window
root = Tk(className='Project 3')
root.geometry("800x680")
root['background'] = '#FFD891'
root.resizable(0, 0)

# label
labelFont = font.Font(weight="bold", size=18)
label = Label(root, text="Traveling and Shipment Routing Using Genetic Algorithm",
            anchor="w", justify="left", font=labelFont, bg='#FFD891')
label.place(x=20, y=15)

# graph entry
graphEntry = Entry(root, highlightthickness=2)
graphEntry.config(highlightbackground="#FFC32D", highlightcolor="#FFC32D")
graphEntry.place(x=50, y=65, width=250, height=120)

# create graph button
buttonFrame = Frame(bd=0, background='#ffffff')
buttonFrame.place(x=99, y=197, relwidth=0.161, relheight=0.079, anchor="nw")
createButton = Button(root, text="Create Graph", bg='#ED7D31', fg='#ffffff',
                    width=13, height=2, borderwidth=0, command=create)
buttonFont = font.Font(size=13)
createButton['font'] = buttonFont
createButton.place(x=102, y=200)

# arrow image
image = PhotoImage(file="arrow.PNG")
imagelabel = Label(root, image=image, bd=0, width=100,height=40)
imagelabel.place(x=330, y=110)

# graph label
graphlabel = Label(root, image=None, bg='#FFD891')
graphlabel.place(x=450, y=55)

# plot label
plotlabel = Label(root, image=None, bg='#FFD891')
plotlabel.place(x=420, y=310)

# white frame
frame = Frame(bd=0, highlightthickness=2, background='#ffffff', highlightbackground="#F1944E", highlightcolor="#F1944E")
frame.place(x=50, y=260, relwidth=0.44, relheight=0.545, anchor="nw")

# frame1
frame1 = Frame(bd=0, highlightthickness=7, background='#ffffff', highlightbackground="#F5C8A6", highlightcolor="#F5C8A6")
frame1.place(x=53, y=263, relwidth=0.432, relheight=0.174, anchor="nw")
frame11 = Frame(bd=0, highlightthickness=2, background='#ffffff', highlightbackground="#4F3C2E", highlightcolor="#4F3C2E")
frame11.place(x=57, y=268, relwidth=0.423, relheight=0.16, anchor="nw")
frame111 = Frame(bd=0, highlightthickness=4, background='#ffffff', highlightbackground="#F5C8A6", highlightcolor="#F5C8A6")
frame111.place(x=59, y=270, relwidth=0.418, relheight=0.154, anchor="nw")

# frame2
frame2 = Frame(bd=0, highlightthickness=7, background='#ffffff', highlightbackground="#F5C8A6", highlightcolor="#F5C8A6")
frame2.place(x=53, y=538, relwidth=0.432, relheight=0.132, anchor="nw")
frame22 = Frame(bd=0, highlightthickness=2, background='#ffffff', highlightbackground="#4F3C2E", highlightcolor="#4F3C2E")
frame22.place(x=57, y=543, relwidth=0.423, relheight=0.118, anchor="nw")
frame222 = Frame(bd=0, highlightthickness=4, background='#ffffff', highlightbackground="#F5C8A6", highlightcolor="#F5C8A6")
frame222.place(x=59, y=545, relwidth=0.418, relheight=0.112, anchor="nw")

# stopping criteria label
font1 = font.Font(weight="bold", size=15)
label1 = Label(root, text="Stopping", font=font1, bg='#ffffff')
label1.place(x=63, y=280)
label2 = Label(root, text="criteria", font=font1, bg='#ffffff')
label2.place(x=68, y=310)

# stopping criteria radiobutton
stoppingCriteria = IntVar()
font2 = font.Font(size=15)
radioButton1 = Radiobutton(root, text='Saturation', variable=stoppingCriteria, value=1,
                        bg='#ffffff', font=font2, selectcolor="#5B9BD5", borderwidth=0)
radioButton1.place(x=175, y=275)
radioButton2 = Radiobutton(root, text='After Generation', variable=stoppingCriteria, value=2,
                        bg='#ffffff', font=font2, selectcolor="#5B9BD5", borderwidth=0)
radioButton2.place(x=175, y=305)

# generation entry
font3 = font.Font(size=14)
generationEntry = Entry(root, highlightthickness=1, fg="white", font=font3, justify='center')
generationEntry.config(background="#5B9BD5")
generationEntry.insert(0, "00")
generationEntry.bind("<FocusIn>", on_entry_click)
generationEntry.bind("<FocusOut>", on_focus_out)
generationEntry.place(x=190, y=340, width=150, height=30)

# population label
label2 = Label(root, text="Population", font=font1, bg='#ffffff')
label2.place(x=60, y=385)

# population entry
populationEntry = Entry(root, highlightthickness=1, fg="white", font=font3, justify='center')
populationEntry.config(background="#5B9BD5")
populationEntry.insert(0, "00")
populationEntry.bind("<FocusIn>", on_entry_click1)
populationEntry.bind("<FocusOut>", on_focus_out1)
populationEntry.place(x=190, y=385, width=150, height=30)

# crossover label
label3 = Label(root, text="Crossover", font=font1, bg='#ffffff')
label3.place(x=60, y=425)

# population entry
crossoverEntry = Entry(root, highlightthickness=1, fg="white", font=font3, justify='center')
crossoverEntry.config(background="#5B9BD5")
crossoverEntry.insert(0, "%")
crossoverEntry.bind("<FocusIn>", on_entry_click2)
crossoverEntry.bind("<FocusOut>", on_focus_out2)
crossoverEntry.place(x=190, y=425, width=150, height=30)

# mutation label
label4 = Label(root, text="Mutation", font=font1, bg='#ffffff')
label4.place(x=60, y=465)

# mutation entry
mutationEntry = Entry(root, highlightthickness=1, fg="white", font=font3, justify='center')
mutationEntry.config(background="#5B9BD5")
mutationEntry.insert(0, "%")
mutationEntry.bind("<FocusIn>", on_entry_click3)
mutationEntry.bind("<FocusOut>", on_focus_out3)
mutationEntry.place(x=190, y=465, width=150, height=30)

# elitism label
label5 = Label(root, text="Elitism", font=font1, bg='#ffffff')
label5.place(x=60, y=505)

# elitism entry
elitismEntry = Entry(root, highlightthickness=1, fg="white", font=font3, justify='center')
elitismEntry.config(background="#5B9BD5")
elitismEntry.insert(0, "%")
elitismEntry.bind("<FocusIn>", on_entry_click4)
elitismEntry.bind("<FocusOut>", on_focus_out4)
elitismEntry.place(x=190, y=505, width=150, height=30)

# selection label
label6 = Label(root, text="Selection", font=font1, bg='#ffffff')
label6.place(x=64, y=565)

# selection radiobutton
selection = IntVar()
font3 = font.Font(size=15)
radioButton3 = Radiobutton(root, text='Ranking', variable=selection, value=1,
                        bg='#ffffff', font=font2, selectcolor="#5B9BD5", borderwidth=0)
radioButton3.place(x=175, y=550)
radioButton4 = Radiobutton(root, text='Tournament', variable=selection, value=2,
                        bg='#ffffff', font=font2, selectcolor="#5B9BD5", borderwidth=0)
radioButton4.place(x=175, y=583)

# solve button
buttonFrame1 = Frame(bd=0, background='#ffffff')
buttonFrame1.place(x=137, y=634, relwidth=0.194, relheight=0.061, anchor="nw")
solveButton = Button(root, text="solve", bg='#ED7D31', fg='#ffffff',
                    width=13, height=1, borderwidth=0, command=slove)
buttonFont1 = font.Font(size=14)
solveButton['font'] = buttonFont1
solveButton.place(x=140, y=637)

root.mainloop()
