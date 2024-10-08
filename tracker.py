import tkinter as tk
from tkinter import ttk
from bs4 import BeautifulSoup
import requests
import webbrowser
from collections import defaultdict

# Function to fetch and parse team standings
def fetch_team_standings():
    url = 'https://stats.sharksice.timetoscore.com/display-stats.php?league=1'
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    divisions = soup.find_all('table')
    team_standings_data = []

    for element in soup.find_all('table'):
        rows = element.find_all('tr')
        for row in rows[1:]:  # Skip the header row
            cols = row.find_all('td')
            if len(cols) >= 7:
                try:
                    team = cols[0].text.strip()
                    gp = int(cols[1].text.strip())
                    w = int(cols[2].text.strip())
                    l = int(cols[3].text.strip())
                    t = int(cols[4].text.strip())
                    otl = int(cols[5].text.strip())
                    pts = int(cols[6].text.strip())
                    team_standings_data.append([team, gp, w, l, t, otl, pts])
                except ValueError as e:
                    print(f"Skipping row due to error: {e}")
                    continue
    display_team_standings(team_standings_data)

# Function to display team standings in the table
def display_team_standings(team_standings_data):
    for i in team_tree.get_children():
        team_tree.delete(i)
    for stats in team_standings_data:
        team_tree.insert("", "end", values=stats)
    print("Team standings displayed.")

# Function to fetch and parse player stats along with their unique profile URLs
def fetch_player_stats(division_url):
    response = requests.get(division_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    rows = soup.find_all('tr')
    player_stats_data = []

    for row in rows[1:]:  # Skip the header row
        cols = row.find_all('td')
        if len(cols) >= 7:
            try:
                player = cols[0].text.strip()  # Player name
                player_link = cols[0].find('a')['href']  # Player profile link
                gp = int(cols[3].text.strip())  # Games played
                goals = int(cols[4].text.strip())  # Goals
                assists = int(cols[5].text.strip())  # Assists
                points = int(cols[6].text.strip())  # Points
                pim = int(cols[7].text.strip())  # Penalty minutes
                
                # Ignore the Pts/Game column here to prevent the error
                if 'Pts/Game' not in cols:
                    badge = assign_badge(gp, goals, assists, pim)  # Assign badge based on stats
                    player_stats_data.append([player, player_link, gp, goals, assists, points, pim, badge])
            except (ValueError, TypeError) as e:
                print(f"Skipping row due to error: {e}")
                continue
    display_player_stats(player_stats_data)
    update_all_time_stats(player_stats_data)
    return player_stats_data

# Function to display player stats in the table
def display_player_stats(player_stats_data):
    for i in player_tree.get_children():
        player_tree.delete(i)
    for stats in player_stats_data:
        player_tree.insert("", "end", values=stats[:1] + stats[2:])  # Skipping link for display
    print("Player stats displayed.")

# Function to handle double-clicking on a player's name and open their unique profile page
def on_player_double_click(event):
    selected_item = player_tree.selection()[0]
    player_link = player_tree.item(selected_item)['values'][1]
    webbrowser.open(player_link)

# Function to assign a badge based on player stats
def assign_badge(gp, goals, assists, pim):
    if pim > 100:
        return "Goon"
    elif pim > 50:
        return "Sinbad"
    elif goals == 0:
        return "McBambii"
    elif assists > goals and assists > 50:
        return "Steve Jobs"
    elif gp < 5:
        return "Duster"
    elif goals > 50:
        return "Lamp Lighter"
    elif assists > 50:
        return "Plumber"
    elif goals > 50 and assists > 50:
        return "All Star"
    elif pim > 75:
        return "Pylon"
    else:
        return "Bender"

# Function to update All-Time Stats for a division
def update_all_time_stats(player_stats_data):
    top_games_played = sorted(player_stats_data, key=lambda x: x[2], reverse=True)[:5]
    top_goals = sorted(player_stats_data, key=lambda x: x[3], reverse=True)[:5]
    top_assists = sorted(player_stats_data, key=lambda x: x[4], reverse=True)[:5]
    top_pim = sorted(player_stats_data, key=lambda x: x[6], reverse=True)[:5]

    worst_players = sorted(player_stats_data, key=lambda x: x[6], reverse=True)[:5]  # Players with the most PIM

    for i in all_time_games_played_tree.get_children():
        all_time_games_played_tree.delete(i)
    for stats in top_games_played:
        all_time_games_played_tree.insert("", "end", values=[stats[0], stats[2]])

    for i in all_time_goals_tree.get_children():
        all_time_goals_tree.delete(i)
    for stats in top_goals:
        all_time_goals_tree.insert("", "end", values=[stats[0], stats[3]])

    for i in all_time_assists_tree.get_children():
        all_time_assists_tree.delete(i)
    for stats in top_assists:
        all_time_assists_tree.insert("", "end", values=[stats[0], stats[4]])

    for i in all_time_pim_tree.get_children():
        all_time_pim_tree.delete(i)
    for stats in top_pim:
        all_time_pim_tree.insert("", "end", values=[stats[0], stats[6]])

    for i in worst_players_tree.get_children():
        worst_players_tree.delete(i)
    for stats in worst_players:
        worst_players_tree.insert("", "end", values=[stats[0], stats[6]])

# Function to aggregate stats across all divisions
def aggregate_stats_across_divisions():
    combined_stats = defaultdict(lambda: [0, 0, 0, 0, 0])

    for division_url in division_urls.values():
        player_stats_data = fetch_player_stats(division_url)
        for stats in player_stats_data:
            player = stats[0]
            combined_stats[player][0] += stats[2]  # Games played
            combined_stats[player][1] += stats[3]  # Goals
            combined_stats[player][2] += stats[4]  # Assists
            combined_stats[player][3] += stats[5]  # Points
            combined_stats[player][4] += stats[6]  # Penalty minutes

    sorted_combined_stats = sorted(combined_stats.items(), key=lambda x: (x[1][0], x[1][1], x[1][2]), reverse=True)
    return sorted_combined_stats[:5]

# Display function for top 5 players across all divisions
def display_top_5_all_time():
    top_5_stats = aggregate_stats_across_divisions()

    for i in top_3_all_time_tree.get_children():
        top_3_all_time_tree.delete(i)
    for player, stats in top_5_stats:
        top_3_all_time_tree.insert("", "end", values=[player, stats[0], stats[1], stats[2], stats[4]])

    division_combobox.set("All Divisions")

# GUI Setup
root = tk.Tk()
root.title("Hockey League Stats")
root.geometry("900x700")

# Team Standings Section
team_tree = ttk.Treeview(root, columns=("Team", "GP", "W", "L", "T", "OTL", "PTS"), show="headings", height=6)
team_tree.heading("Team", text="Team")
team_tree.heading("GP", text="GP")
team_tree.heading("W", text="W")
team_tree.heading("L", text="L")
team_tree.heading("T", text="T")
team_tree.heading("OTL", text="OTL")
team_tree.heading("PTS", text="PTS")

team_tree.column("Team", width=150, anchor=tk.W)
for col in ["GP", "W", "L", "T", "OTL", "PTS"]:
    team_tree.column(col, width=60, anchor=tk.CENTER)

team_tree.pack()

view_team_button = ttk.Button(root, text="View Team Standings", command=fetch_team_standings)
view_team_button.pack()

# Player Stats Section
player_tree = ttk.Treeview(root, columns=("Player", "GP", "Goals", "Assists", "Points", "PIM", "Badge"), show="headings", height=6)
player_tree.heading("Player", text="Player")
player_tree.heading("GP", text="GP")
player_tree.heading("Goals", text="Goals")
player_tree.heading("Assists", text="Assists")
player_tree.heading("Points", text="Points")
player_tree.heading("PIM", text="PIM")
player_tree.heading("Badge", text="Badge")

player_tree.column("Player", width=150, anchor=tk.W)
for col in ["GP", "Goals", "Assists", "Points", "PIM", "Badge"]:
    player_tree.column(col, width=60, anchor=tk.CENTER)

player_tree.bind("<Double-1>", on_player_double_click)  # Bind double-click to open player page
player_tree.pack()

# Dropdown to select division and fetch player stats
division_combobox = ttk.Combobox(root, values=[
    "Adult Division 1", "Adult Division 2", "Adult Division 3A", "Adult Division 3B", "Adult Division 4A", 
    "Adult Division 4B", "Adult Division 5A", "Adult Division 5B", "Adult Division 6A", "Adult Division 6B", 
    "Adult Division 7A", "Adult Division 7 East", "Adult Division 7 West", "Adult Division 8A", 
    "Adult Division 8B East", "Adult Division 8B West", "Adult Division 9"
])
division_combobox.current(0)
division_combobox.pack()

# Button to fetch and display player stats for the selected division
division_urls = {
    "Adult Division 1": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=221&conf=0',
    "Adult Division 2": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=222&conf=0',
    "Adult Division 3A": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=223&conf=0',
    "Adult Division 3B": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=224&conf=0',
    "Adult Division 4A": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=225&conf=0',
    "Adult Division 4B": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=235&conf=0',
    "Adult Division 5A": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=226&conf=0',
    "Adult Division 5B": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=227&conf=0',
    "Adult Division 6A": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=228&conf=0',
    "Adult Division 6B": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=229&conf=0',
    "Adult Division 7A": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=230&conf=0',
    "Adult Division 7 East": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=231&conf=4',
    "Adult Division 7 West": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=231&conf=5',
    "Adult Division 8A": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=302&conf=0',
    "Adult Division 8B East": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=303&conf=4',
    "Adult Division 8B West": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=303&conf=5',
    "Adult Division 9": 'https://stats.sharksice.timetoscore.com/display-league-stats?stat_class=1&league=1&season=66&level=233&conf=0'
}

def view_player_stats():
    selected_division = division_combobox.get()
    if selected_division != "All Divisions":
        division_url = division_urls.get(selected_division)
        if division_url:
            player_stats_data = fetch_player_stats(division_url)
            update_all_time_stats(player_stats_data)

view_player_button = ttk.Button(root, text="View Player Stats", command=view_player_stats)
view_player_button.pack()

# All-Time Stats Section
all_time_frame = tk.LabelFrame(root, text="All-Time Stats - By Division")
all_time_frame.pack(pady=10)

top_frame = tk.Frame(all_time_frame)
top_frame.pack()

all_time_games_played_tree = ttk.Treeview(top_frame, columns=("Player", "Games Played"), show="headings", height=5)
all_time_games_played_tree.heading("Player", text="Player")
all_time_games_played_tree.heading("Games Played", text="Games Played")
all_time_games_played_tree.column("Player", anchor=tk.CENTER)
all_time_games_played_tree.column("Games Played", anchor=tk.CENTER)
all_time_games_played_tree.pack(side=tk.LEFT, padx=10)

all_time_goals_tree = ttk.Treeview(top_frame, columns=("Player", "Goals"), show="headings", height=5)
all_time_goals_tree.heading("Player", text="Player")
all_time_goals_tree.heading("Goals", text="Goals")
all_time_goals_tree.column("Player", anchor=tk.CENTER)
all_time_goals_tree.column("Goals", anchor=tk.CENTER)
all_time_goals_tree.pack(side=tk.LEFT, padx=10)

bottom_frame = tk.Frame(all_time_frame)
bottom_frame.pack(pady=10)

all_time_assists_tree = ttk.Treeview(bottom_frame, columns=("Player", "Assists"), show="headings", height=5)
all_time_assists_tree.heading("Player", text="Player")
all_time_assists_tree.heading("Assists", text="Assists")
all_time_assists_tree.column("Player", anchor=tk.CENTER)
all_time_assists_tree.column("Assists", anchor=tk.CENTER)
all_time_assists_tree.pack(side=tk.LEFT, padx=10)

all_time_pim_tree = ttk.Treeview(bottom_frame, columns=("Player", "Penalty Minutes"), show="headings", height=5)
all_time_pim_tree.heading("Player", text="Player")
all_time_pim_tree.heading("Penalty Minutes", text="Penalty Minutes")
all_time_pim_tree.column("Player", anchor=tk.CENTER)
all_time_pim_tree.column("Penalty Minutes", anchor=tk.CENTER)
all_time_pim_tree.pack(side=tk.LEFT, padx=10)

# Worst Players (Top 5) Section
worst_players_frame = tk.LabelFrame(root, text="Worst Players - Top 5 (By Penalty Minutes)")
worst_players_frame.pack(pady=10)

worst_players_tree = ttk.Treeview(worst_players_frame, columns=("Player", "Penalty Minutes"), show="headings", height=5)
worst_players_tree.heading("Player", text="Player")
worst_players_tree.heading("Penalty Minutes", text="Penalty Minutes")
worst_players_tree.column("Player", anchor=tk.CENTER)
worst_players_tree.column("Penalty Minutes", anchor=tk.CENTER)
worst_players_tree.pack(side=tk.LEFT, padx=10)

# All-Time Top 5 Players Across All Divisions Section
top_3_all_time_frame = tk.LabelFrame(root, text="Top 5 Players of All Time Across All Divisions")
top_3_all_time_frame.pack(pady=10)

top_3_all_time_tree = ttk.Treeview(top_3_all_time_frame, columns=("Player", "GP", "Goals", "Assists", "PIM"), show="headings", height=5)
top_3_all_time_tree.heading("Player", text="Player")
top_3_all_time_tree.heading("GP", text="GP")
top_3_all_time_tree.heading("Goals", text="Goals")
top_3_all_time_tree.heading("Assists", text="Assists")
top_3_all_time_tree.heading("PIM", text="PIM")
top_3_all_time_tree.column("Player", anchor=tk.CENTER)
top_3_all_time_tree.column("GP", anchor=tk.CENTER)
top_3_all_time_tree.column("Goals", anchor=tk.CENTER)
top_3_all_time_tree.column("Assists", anchor=tk.CENTER)
top_3_all_time_tree.column("PIM", anchor=tk.CENTER)
top_3_all_time_tree.pack()

view_all_time_button = ttk.Button(root, text="View Top 5 Players Across All Divisions", command=display_top_5_all_time)
view_all_time_button.pack(pady=10)

# Legend Section
legend = tk.Label(root, text="Legend: GP - Games Played, Goals - Goals Scored, Assists - Assists, PIM - Penalty Minutes")
legend.pack(pady=10)

root.mainloop()
