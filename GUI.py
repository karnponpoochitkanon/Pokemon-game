import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

df = pd.read_csv("game_stats.csv", on_bad_lines='skip')
df.columns = df.columns.str.strip()
sns.set(style="darkgrid")

features = {
    "Distance Histogram": lambda ax: sns.histplot(df["Distance"], kde=True, bins=15, color="#69b3a2", edgecolor="black", ax=ax),
    "Play Time Line Chart": lambda ax: sns.lineplot(x=range(len(df)), y=df["Time(s)"], ax=ax),
    "Character Pie Chart": lambda ax: ax.pie(df["Character"].value_counts(), labels=df["Character"].value_counts().index,
                                             autopct="%1.1f%%", colors=["lightcoral", "turquoise", "gold"]),
    "Pokemon Count Bar": lambda ax: sns.barplot(x=df["Total Pokemon"].value_counts().sort_index().index,
                                                y=df["Total Pokemon"].value_counts().sort_index().values, palette="Blues", ax=ax),
    "Heal Tree Usage": lambda ax: sns.barplot(x=df["Heal Tree Uses"].value_counts().sort_index().index,
                                              y=df["Heal Tree Uses"].value_counts().sort_index().values, palette="Greens", ax=ax),
    "YIM Battle Histogram": lambda ax: sns.histplot(df["YIM Battles"], bins=range(1, df["YIM Battles"].max()+2),
                                                    color="salmon", edgecolor="black", ax=ax),
    "Total Pokemon vs Time": lambda ax: sns.scatterplot(data=df, x="Total Pokemon", y="Time(s)", ax=ax, color="skyblue", edgecolor="black"),
    "Total Pokemon vs Distance": lambda ax: sns.scatterplot(data=df, x="Total Pokemon", y="Distance", ax=ax, color="goldenrod", edgecolor="black"),
}

graph_descriptions = {
    "Distance Histogram": "This histogram shows how far players walked during the game. Most walked between 3000–5500 units.",
    "Play Time Line Chart": "This line chart displays the total time (in seconds) each player spent in the game.",
    "Character Pie Chart": "This pie chart shows the percentage of players who selected each character.",
    "Pokemon Count Bar": "This bar chart shows how many Pokémon each player had. Most players had around 5 to 10 Pokemon.",
    "Heal Tree Usage": "This bar chart shows how many times players used the healing tree. The majority used it 1 or 2 times.",
    "YIM Battle Histogram": "This histogram shows the number of YIM boss battles each player engaged in.",
    "Total Pokemon vs Time": "This scatter plot compares the number of Pokémon with total playtime. Patterns may reveal time investment vs reward.",
    "Total Pokemon vs Distance": "This scatter plot compares how far players walked with how many Pokemon they collected.",
}

def get_summary_df():
    cols = ["Time(s)", "YIM Battles", "Distance", "Total Pokemon", "Heal Tree Uses"]
    summary = df[cols].describe().T
    summary["mode"] = df[cols].mode().iloc[0]
    return summary.reset_index().rename(columns={"index": "Feature"})

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Game Statistics Dashboard")
        self.geometry("1000x700")
        self.configure(bg="#f9f9f9")

        self.main_frame = tk.Frame(self, bg="#f9f9f9")
        self.graph_frame = tk.Frame(self, bg="#f9f9f9")

        self.build_main_menu()

    def build_main_menu(self):
        self.clear_frame()
        self.main_frame.pack(fill="both", expand=True)
        tk.Label(self.main_frame, text="Game Statistics Dashboard", font=("Arial", 20, "bold"), bg="#f9f9f9").pack(pady=20)

        for name in features:
            tk.Button(self.main_frame, text=name, font=("Arial", 12), width=35,
                      command=lambda n=name: self.show_feature(n)).pack(pady=5)

        spacer = tk.Frame(self.main_frame, bg="#f9f9f9")
        spacer.pack(expand=True)

        exit_btn = tk.Button(self.main_frame, text="❌ Exit Program", font=("Arial", 12), width=35, bg="#f2f2f2", command=self.quit)
        exit_btn.pack(pady=20)

    def show_feature(self, name):
        self.clear_frame()
        self.graph_frame.pack(fill="both", expand=True)

        if name == "Summary Table":
            self.build_summary_table()
        else:
            fig, ax = plt.subplots(figsize=(6.5, 4.5))
            features[name](ax)
            ax.set_title(name)
            canvas = FigureCanvasTkAgg(fig, master=self.graph_frame)
            canvas.draw()
            canvas.get_tk_widget().pack(fill="both", expand=True)

            if name in graph_descriptions:
                desc = tk.Label(self.graph_frame, text=graph_descriptions[name], font=("Arial", 11), bg="#f9f9f9", wraplength=900)
                desc.pack(pady=(5, 15))

        tk.Button(self.graph_frame, text="← Back to Menu", font=("Arial", 12), command=self.build_main_menu).pack(pady=10, side="bottom")

    def build_summary_table(self):
        df_summary = get_summary_df()
        style = ttk.Style()
        style.theme_use("default")
        style.configure("Treeview", background="white", foreground="black", rowheight=25, fieldbackground="white", bordercolor="black")
        style.configure("Treeview.Heading", font=("Arial", 10, "bold"), background="#f0f0f0", relief="raised")

        tree = ttk.Treeview(self.graph_frame, show='headings', style="Treeview")
        tree["columns"] = list(df_summary.columns)
        for col in df_summary.columns:
            tree.heading(col, text=col)
            tree.column(col, anchor=tk.CENTER, width=100)
        for _, row in df_summary.iterrows():
            tree.insert("", "end", values=list(row.round(2)))
        tree.pack(fill="both", expand=True, padx=10, pady=10)

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        for widget in self.graph_frame.winfo_children():
            widget.destroy()
        self.main_frame.pack_forget()
        self.graph_frame.pack_forget()

App().mainloop()