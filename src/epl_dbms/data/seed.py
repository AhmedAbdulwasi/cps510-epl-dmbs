"""
Expanded Premier League seed data for Populate Tables.

Attribute ratings are approximate public-facing estimates for coursework
(not an official EA Sports / FIFA dump). Dates use DD-MM-YYYY strings
that the populate helper converts with TO_DATE.
"""

from __future__ import annotations

# Stadium_Name, Stadium_Capacity
STADIUMS: list[tuple[str, int]] = [
    ("Emirates Stadium", 60704),
    ("American Express Stadium", 31876),
    ("Etihad Stadium", 53400),
    ("Anfield", 61276),
    ("Vitality Stadium", 11307),
    ("Gtech Community Stadium", 17250),
    ("Elland Road", 37608),
    ("Stamford Bridge", 40341),
    ("Goodison Park", 39414),
    ("Tottenham Hotspur Stadium", 62850),
    ("MKM Stadium", 25586),
    ("Villa Park", 42640),
    ("St James' Park", 52305),
    ("Coventry Building Society Arena", 32609),
    ("Craven Cottage", 25700),
    ("Portman Road", 30000),
    ("City Ground", 30404),
    ("Stadium of Light", 49000),
    ("Old Trafford", 74158),
    ("Selhurst Park", 25486),
]

# Team_ID, Club_Name, Valuation, Stadium_Name, Year_Founded, Crest, City
CLUBS: list[tuple[str, str, int, str, int, str, str]] = [
    ("AR", "Arsenal FC", 3100000000, "Emirates Stadium", 1886, "crest_arsenal", "London"),
    ("BH", "Brighton & Hove Albion", 900000000, "American Express Stadium", 1901, "crest_brighton", "Brighton"),
    ("MC", "Manchester City", 5000000000, "Etihad Stadium", 1880, "crest_man_city", "Manchester"),
    ("LV", "Liverpool FC", 4700000000, "Anfield", 1892, "crest_liverpool", "Liverpool"),
    ("BO", "AFC Bournemouth", 450000000, "Vitality Stadium", 1899, "crest_bournemouth", "Bournemouth"),
    ("BR", "Brentford FC", 500000000, "Gtech Community Stadium", 1889, "crest_brentford", "London"),
    ("LE", "Leeds United", 550000000, "Elland Road", 1919, "crest_leeds", "Leeds"),
    ("CH", "Chelsea FC", 3200000000, "Stamford Bridge", 1905, "crest_chelsea", "London"),
    ("EV", "Everton FC", 700000000, "Goodison Park", 1878, "crest_everton", "Liverpool"),
    ("TH", "Tottenham Hotspur", 2800000000, "Tottenham Hotspur Stadium", 1882, "crest_tottenham", "London"),
    ("HU", "Hull City", 180000000, "MKM Stadium", 1904, "crest_hull", "Hull"),
    ("AV", "Aston Villa", 1100000000, "Villa Park", 1874, "crest_villa", "Birmingham"),
    ("NE", "Newcastle United", 1500000000, "St James' Park", 1892, "crest_newcastle", "Newcastle"),
    ("CO", "Coventry City", 160000000, "Coventry Building Society Arena", 1883, "crest_coventry", "Coventry"),
    ("FU", "Fulham FC", 650000000, "Craven Cottage", 1879, "crest_fulham", "London"),
    ("IP", "Ipswich Town", 220000000, "Portman Road", 1878, "crest_ipswich", "Ipswich"),
    ("NF", "Nottingham Forest", 600000000, "City Ground", 1865, "crest_forest", "Nottingham"),
    ("SU", "Sunderland AFC", 250000000, "Stadium of Light", 1879, "crest_sunderland", "Sunderland"),
    ("MU", "Manchester United", 7200000000, "Old Trafford", 1878, "crest_man_united", "Manchester"),
    ("CP", "Crystal Palace", 550000000, "Selhurst Park", 1905, "crest_palace", "London"),
]

# Manager_ID, Name, Team_ID, Date_Joining, Contract_Expiry, Trophies, Salary, DOB, Formation
MANAGERS: list[tuple[str, str, str, str, str, int, int, str, str]] = [
    ("01", "Mikel Arteta", "AR", "22-12-2019", "30-06-2030", 3, 11500000, "26-03-1982", "433"),
    ("02", "Fabian Hürzeler", "BH", "01-07-2024", "30-06-2027", 0, 3500000, "26-02-1993", "343"),
    ("03", "Pep Guardiola", "MC", "01-07-2016", "30-06-2027", 18, 20000000, "18-01-1971", "433"),
    ("04", "Arne Slot", "LV", "01-06-2024", "30-06-2027", 1, 10000000, "17-09-1978", "433"),
    ("05", "Andoni Iraola", "BO", "19-06-2023", "30-06-2026", 0, 3500000, "22-06-1982", "423"),
    ("06", "Keith Andrews", "BR", "01-07-2025", "30-06-2027", 0, 2500000, "13-09-1980", "442"),
    ("07", "Daniel Farke", "LE", "04-07-2023", "30-06-2027", 2, 3000000, "30-10-1976", "433"),
    ("08", "Enzo Maresca", "CH", "01-07-2024", "30-06-2029", 1, 10000000, "10-02-1980", "342"),
    ("09", "David Moyes", "EV", "11-01-2025", "30-06-2027", 1, 5000000, "25-04-1963", "442"),
    ("10", "Thomas Frank", "TH", "01-07-2025", "30-06-2028", 0, 6000000, "09-10-1973", "352"),
    ("11", "Sergej Jakirović", "HU", "01-07-2025", "30-06-2027", 0, 1200000, "23-12-1976", "433"),
    ("12", "Unai Emery", "AV", "01-11-2022", "30-06-2029", 5, 8000000, "03-11-1971", "423"),
    ("13", "Eddie Howe", "NE", "08-11-2021", "30-06-2028", 1, 7000000, "29-11-1977", "433"),
    ("14", "Frank Lampard", "CO", "28-11-2024", "30-06-2027", 0, 2000000, "20-06-1978", "433"),
    ("15", "Marco Silva", "FU", "01-07-2021", "30-06-2026", 0, 4500000, "12-07-1977", "433"),
    ("16", "Kieran McKenna", "IP", "16-12-2021", "30-06-2028", 1, 2500000, "14-05-1986", "423"),
    ("17", "Nuno Espírito Santo", "NF", "20-12-2023", "30-06-2026", 1, 5000000, "25-01-1974", "433"),
    ("18", "Régis Le Bris", "SU", "22-06-2024", "30-06-2027", 1, 2000000, "06-12-1975", "433"),
    ("19", "Ruben Amorim", "MU", "11-11-2024", "30-06-2027", 2, 10000000, "27-01-1985", "343"),
    ("20", "Oliver Glasner", "CP", "19-02-2024", "30-06-2027", 1, 4500000, "28-08-1974", "342"),
]

# Player rows (Player_ID is VARCHAR2(3): P01-P99):
# (Player_ID, Team_ID, Name, Crest, Foot, NAT, DOB, Pos, OVR, Height, Weight,
#  attr_kind, a1, a2, a3, a4, a5, a6)
# attr_kind 'GK' -> Diving, Reflexes, Handling, Positioning, Speed, Kicking
# attr_kind 'OF' -> Pace, Passing, Dribbling, Physicality, Defending, Shooting
PLAYERS: list[tuple] = [
    # --- Arsenal FC ---
    ('P01', 'AR', 'Bukayo Saka', 'crest_arsenal', 'L', 'ENG', '05-09-2001', 'RW', 89, 178, 72, 'OF', 85, 84, 88, 70, 55, 84),
    ('P02', 'AR', 'David Raya', 'crest_arsenal', 'R', 'ESP', '15-09-1995', 'GK', 85, 183, 80, 'GK', 86, 87, 84, 85, 62, 87),
    # --- Manchester United ---
    ('P03', 'MU', 'Bruno Fernandes', 'crest_man_united', 'R', 'POR', '08-09-1994', 'CAM', 87, 179, 69, 'OF', 72, 92, 84, 74, 62, 86),
    # --- Liverpool FC ---
    ('P04', 'LV', 'Virgil van Dijk', 'crest_liverpool', 'R', 'NED', '08-07-1991', 'CB', 89, 193, 92, 'OF', 76, 78, 70, 88, 90, 60),
    # --- Chelsea FC ---
    ('P05', 'CH', 'Cole Palmer', 'crest_chelsea', 'L', 'ENG', '06-05-2002', 'CAM', 88, 185, 74, 'OF', 78, 88, 88, 66, 48, 86),
    # --- Liverpool FC ---
    ('P06', 'LV', 'Alexander Isak', 'crest_liverpool', 'R', 'SWE', '21-09-1999', 'ST', 88, 192, 77, 'OF', 88, 78, 86, 74, 36, 88),
    ('P07', 'LV', 'Alisson Becker', 'crest_liverpool', 'R', 'BRA', '02-10-1992', 'GK', 89, 193, 91, 'GK', 88, 90, 88, 88, 58, 86),
    # --- Manchester United ---
    ('P08', 'MU', 'André Onana', 'crest_man_united', 'R', 'CMR', '02-04-1996', 'GK', 84, 190, 93, 'GK', 84, 86, 80, 80, 58, 90),
    # --- Newcastle United ---
    ('P09', 'NE', 'Anthony Elanga', 'crest_newcastle', 'R', 'SWE', '27-04-2002', 'RW', 80, 178, 72, 'OF', 94, 70, 80, 66, 36, 76),
    # --- AFC Bournemouth ---
    ('P10', 'BO', 'Antoine Semenyo', 'crest_bournemouth', 'R', 'GHA', '07-01-2000', 'RW', 80, 185, 80, 'OF', 88, 70, 80, 80, 42, 78),
    # --- Newcastle United ---
    ('P11', 'NE', 'Bruno Guimarães', 'crest_newcastle', 'R', 'BRA', '16-11-1997', 'CM', 86, 182, 74, 'OF', 74, 86, 86, 78, 78, 76),
    # --- Manchester United ---
    ('P12', 'MU', 'Bryan Mbeumo', 'crest_man_united', 'L', 'CMR', '07-08-1999', 'RW', 84, 171, 68, 'OF', 88, 78, 84, 72, 42, 84),
    # --- Nottingham Forest ---
    ('P13', 'NF', 'Chris Wood', 'crest_forest', 'R', 'NZL', '07-12-1991', 'ST', 80, 191, 92, 'OF', 64, 64, 66, 86, 40, 82),
    # --- Arsenal FC ---
    ('P14', 'AR', 'Declan Rice', 'crest_arsenal', 'R', 'ENG', '14-01-1999', 'CDM', 88, 185, 80, 'OF', 74, 84, 78, 84, 84, 72),
    # --- Aston Villa ---
    ('P15', 'AV', 'Emiliano Martínez', 'crest_villa', 'R', 'ARG', '02-09-1992', 'GK', 88, 195, 88, 'GK', 88, 90, 84, 86, 54, 82),
    # --- Manchester City ---
    ('P16', 'MC', 'Erling Haaland', 'crest_man_city', 'L', 'NOR', '21-07-2000', 'ST', 91, 194, 88, 'OF', 89, 65, 80, 88, 45, 94),
    # --- AFC Bournemouth ---
    ('P17', 'BO', 'Evanilson', 'crest_bournemouth', 'R', 'BRA', '06-10-1999', 'ST', 80, 183, 80, 'OF', 82, 66, 78, 78, 36, 82),
    # --- Liverpool FC ---
    ('P18', 'LV', 'Florian Wirtz', 'crest_liverpool', 'R', 'GER', '03-05-2003', 'CAM', 89, 176, 70, 'OF', 82, 90, 92, 64, 48, 82),
    # --- Tottenham Hotspur ---
    ('P19', 'TH', 'James Maddison', 'crest_tottenham', 'L', 'ENG', '23-11-1996', 'CAM', 84, 175, 73, 'OF', 76, 88, 86, 64, 48, 82),
    # --- Crystal Palace ---
    ('P20', 'CP', 'Jean-Philippe Mateta', 'crest_palace', 'R', 'FRA', '28-06-1997', 'ST', 82, 192, 88, 'OF', 78, 62, 74, 88, 36, 84),
    # --- Everton FC ---
    ('P21', 'EV', 'Jordan Pickford', 'crest_everton', 'L', 'ENG', '07-03-1994', 'GK', 84, 185, 77, 'GK', 84, 86, 78, 82, 60, 86),
    # --- Chelsea FC ---
    ('P22', 'CH', 'João Pedro', 'crest_chelsea', 'R', 'BRA', '26-09-2001', 'ST', 82, 182, 74, 'OF', 80, 76, 84, 72, 40, 82),
    # --- Brighton & Hove Albion ---
    ('P23', 'BH', 'Kaoru Mitoma', 'crest_brighton', 'R', 'JPN', '20-05-1997', 'LW', 84, 178, 71, 'OF', 90, 76, 88, 68, 40, 78),
    # --- Arsenal FC ---
    ('P24', 'AR', 'Martin Ødegaard', 'crest_arsenal', 'L', 'NOR', '17-12-1998', 'CAM', 88, 178, 68, 'OF', 76, 90, 88, 64, 58, 82),
    # --- Nottingham Forest ---
    ('P25', 'NF', 'Morgan Gibbs-White', 'crest_forest', 'R', 'ENG', '27-01-2000', 'CAM', 83, 171, 68, 'OF', 80, 82, 84, 70, 52, 78),
    # --- Aston Villa ---
    ('P26', 'AV', 'Ollie Watkins', 'crest_villa', 'R', 'ENG', '30-12-1995', 'ST', 85, 180, 75, 'OF', 86, 72, 80, 78, 40, 84),
    # --- Chelsea FC ---
    ('P27', 'CH', 'Pedro Neto', 'crest_chelsea', 'L', 'POR', '09-03-2000', 'RW', 83, 172, 64, 'OF', 92, 76, 86, 62, 36, 78),
    # --- Manchester City ---
    ('P28', 'MC', 'Phil Foden', 'crest_man_city', 'L', 'ENG', '28-05-2000', 'CAM', 88, 171, 70, 'OF', 84, 86, 90, 66, 50, 84),
    # --- Arsenal FC ---
    ('P29', 'AR', 'Viktor Gyökeres', 'crest_arsenal', 'R', 'SWE', '04-06-1998', 'ST', 86, 187, 90, 'OF', 86, 72, 80, 88, 42, 86),
    # --- Brentford FC ---
    ('P30', 'BR', 'Yoane Wissa', 'crest_brentford', 'R', 'COD', '03-09-1996', 'ST', 80, 176, 74, 'OF', 86, 68, 78, 74, 36, 82),
    # --- Arsenal FC ---
    ('P31', 'AR', 'William Saliba', 'crest_arsenal', 'R', 'FRA', '24-03-2001', 'CB', 88, 192, 92, 'OF', 82, 72, 70, 84, 88, 48),
    ('P32', 'AR', 'Gabriel Magalhães', 'crest_arsenal', 'L', 'BRA', '19-12-1997', 'CB', 87, 190, 87, 'OF', 75, 68, 62, 86, 87, 45),
    ('P33', 'AR', 'Piero Hincapié', 'crest_arsenal', 'L', 'ECU', '09-01-2002', 'CB', 82, 184, 77, 'OF', 84, 72, 74, 78, 81, 52),
    ('P34', 'AR', 'Jurriën Timber', 'crest_arsenal', 'R', 'NED', '17-06-2001', 'RB', 83, 179, 73, 'OF', 82, 76, 78, 74, 80, 55),
    # --- Brighton & Hove Albion ---
    ('P35', 'BH', 'Bart Verbruggen', 'crest_brighton', 'R', 'NED', '18-08-2002', 'GK', 80, 194, 83, 'GK', 81, 82, 78, 78, 55, 76),
    ('P36', 'BH', 'Lewis Dunk', 'crest_brighton', 'R', 'ENG', '21-11-1991', 'CB', 81, 192, 88, 'OF', 58, 70, 58, 84, 82, 48),
    ('P37', 'BH', 'Jan Paul van Hecke', 'crest_brighton', 'R', 'NED', '08-06-2000', 'CB', 79, 189, 82, 'OF', 72, 68, 64, 80, 80, 45),
    ('P38', 'BH', 'Maxim De Cuyper', 'crest_brighton', 'L', 'BEL', '22-12-2000', 'LB', 78, 182, 75, 'OF', 80, 76, 74, 72, 74, 62),
    # --- Manchester City ---
    ('P39', 'MC', 'Gianluigi Donnarumma', 'crest_man_city', 'R', 'ITA', '25-02-1999', 'GK', 89, 196, 90, 'GK', 90, 90, 84, 86, 58, 78),
    ('P40', 'MC', 'Rúben Dias', 'crest_man_city', 'R', 'POR', '14-05-1997', 'CB', 88, 187, 82, 'OF', 68, 74, 66, 86, 90, 45),
    ('P41', 'MC', 'Joško Gvardiol', 'crest_man_city', 'L', 'CRO', '23-01-2002', 'CB', 86, 185, 80, 'OF', 82, 78, 76, 84, 84, 58),
    ('P42', 'MC', "Nico O'Reilly", 'crest_man_city', 'L', 'ENG', '21-03-2005', 'CM', 74, 177, 70, 'OF', 76, 76, 78, 68, 64, 66),
    # --- Liverpool FC ---
    ('P43', 'LV', 'Ronald Araújo', 'crest_liverpool', 'R', 'URU', '07-03-1999', 'CB', 86, 188, 79, 'OF', 82, 66, 64, 86, 86, 48),
    ('P44', 'LV', 'Andrew Robertson', 'crest_liverpool', 'L', 'SCO', '11-03-1994', 'LB', 84, 178, 64, 'OF', 84, 82, 78, 76, 78, 62),
    ('P45', 'LV', 'Jeremie Frimpong', 'crest_liverpool', 'R', 'NED', '10-12-2000', 'RB', 84, 171, 64, 'OF', 94, 76, 84, 68, 68, 68),
    ('P46', 'LV', 'Ryan Gravenberch', 'crest_liverpool', 'R', 'NED', '16-05-2002', 'CM', 84, 190, 77, 'OF', 78, 82, 84, 80, 76, 74),
    # --- AFC Bournemouth ---
    ('P47', 'BO', 'Justin Kluivert', 'crest_bournemouth', 'R', 'NED', '05-05-1999', 'LW', 80, 171, 66, 'OF', 86, 74, 84, 64, 38, 78),
    ('P48', 'BO', 'Marcus Tavernier', 'crest_bournemouth', 'L', 'ENG', '22-03-1999', 'LM', 78, 178, 70, 'OF', 82, 76, 78, 70, 52, 74),
    ('P49', 'BO', 'Lewis Cook', 'crest_bournemouth', 'R', 'ENG', '08-02-1997', 'CM', 78, 175, 71, 'OF', 72, 78, 74, 74, 74, 66),
    ('P50', 'BO', 'Eli Junior Kroupi', 'crest_bournemouth', 'R', 'FRA', '23-06-2006', 'ST', 72, 179, 72, 'OF', 78, 64, 74, 66, 30, 74),
    # --- Brentford FC ---
    ('P51', 'BR', 'Kristoffer Ajer', 'crest_brentford', 'R', 'NOR', '17-04-1998', 'CB', 78, 198, 92, 'OF', 74, 66, 62, 84, 78, 42),
    ('P52', 'BR', 'Keane Lewis-Potter', 'crest_brentford', 'R', 'ENG', '22-02-2001', 'LW', 76, 170, 68, 'OF', 86, 70, 78, 64, 36, 74),
    ('P53', 'BR', 'Fábio Carvalho', 'crest_brentford', 'R', 'POR', '30-08-2002', 'CAM', 76, 170, 64, 'OF', 80, 76, 82, 58, 40, 74),
    ('P54', 'BR', 'Igor Thiago', 'crest_brentford', 'R', 'BRA', '26-06-2001', 'ST', 78, 191, 88, 'OF', 78, 62, 72, 84, 34, 80),
    # --- Leeds United ---
    ('P55', 'LE', 'James Trafford', 'crest_leeds', 'R', 'ENG', '10-10-2002', 'GK', 78, 197, 85, 'GK', 78, 80, 74, 76, 52, 72),
    ('P56', 'LE', 'Sean Longstaff', 'crest_leeds', 'R', 'ENG', '30-10-1997', 'CM', 76, 187, 74, 'OF', 70, 76, 72, 76, 72, 68),
    ('P57', 'LE', 'Dominic Calvert-Lewin', 'crest_leeds', 'R', 'ENG', '16-03-1997', 'ST', 78, 187, 71, 'OF', 78, 64, 72, 84, 42, 78),
    ('P58', 'CP', 'Ismaïla Sarr', 'crest_palace', 'R', 'SEN', '25-02-1998', 'RW', 82, 185, 76, 'OF', 94, 72, 82, 74, 36, 80),
    # --- Chelsea FC ---
    ('P59', 'CH', 'Robert Sánchez', 'crest_chelsea', 'R', 'ESP', '18-11-1997', 'GK', 80, 197, 90, 'GK', 80, 82, 78, 78, 50, 74),
    ('P60', 'CH', 'Reece James', 'crest_chelsea', 'R', 'ENG', '08-12-1999', 'RB', 84, 182, 82, 'OF', 82, 84, 80, 84, 80, 70),
    ('P61', 'CH', 'Malo Gusto', 'crest_chelsea', 'R', 'FRA', '19-05-2003', 'RB', 80, 178, 70, 'OF', 88, 76, 80, 70, 74, 58),
    ('P62', 'CH', 'Wesley Fofana', 'crest_chelsea', 'R', 'FRA', '17-12-2000', 'CB', 82, 190, 84, 'OF', 84, 64, 62, 84, 84, 40),
    # --- Everton FC ---
    ('P63', 'EV', 'Iliman Ndiaye', 'crest_everton', 'R', 'SEN', '06-03-2000', 'CAM', 80, 180, 72, 'OF', 84, 76, 86, 66, 42, 78),
    ('P64', 'EV', 'Kiernan Dewsbury-Hall', 'crest_everton', 'L', 'ENG', '06-09-1998', 'CM', 78, 178, 72, 'OF', 74, 80, 80, 72, 68, 72),
    # --- Tottenham Hotspur ---
    ('P65', 'TH', 'Guglielmo Vicario', 'crest_tottenham', 'R', 'ITA', '07-10-1996', 'GK', 84, 194, 83, 'GK', 84, 86, 80, 82, 52, 74),
    ('P66', 'TH', 'Pedro Porro', 'crest_tottenham', 'R', 'ESP', '13-09-1999', 'RB', 83, 173, 69, 'OF', 84, 82, 80, 70, 74, 72),
    ('P67', 'TH', 'Micky van de Ven', 'crest_tottenham', 'L', 'NED', '19-04-2001', 'CB', 85, 193, 81, 'OF', 92, 68, 66, 82, 84, 42),
    ('P68', 'TH', 'Radu Drăgușin', 'crest_tottenham', 'R', 'ROU', '03-02-2002', 'CB', 78, 191, 85, 'OF', 72, 62, 58, 82, 80, 40),
    # --- Hull City ---
    ('P69', 'HU', 'Zion Suzuki', 'crest_hull', 'R', 'JPN', '21-08-2002', 'GK', 74, 190, 84, 'GK', 74, 76, 72, 72, 48, 68),
    ('P70', 'HU', 'Liam Millar', 'crest_hull', 'L', 'CAN', '27-09-1999', 'LW', 74, 180, 74, 'OF', 86, 68, 76, 68, 36, 70),
    ('P71', 'HU', 'Aaron Wan-Bissaka', 'crest_hull', 'R', 'ENG', '26-11-1997', 'RB', 78, 183, 72, 'OF', 84, 64, 72, 74, 82, 42),
    # --- Aston Villa ---
    ('P72', 'AV', 'Matty Cash', 'crest_villa', 'R', 'POL', '07-08-1997', 'RB', 80, 185, 76, 'OF', 84, 72, 74, 78, 76, 64),
    ('P73', 'AV', 'Tyrone Mings', 'crest_villa', 'L', 'ENG', '13-03-1993', 'CB', 78, 196, 84, 'OF', 68, 66, 58, 84, 80, 40),
    ('P74', 'AV', 'Ezri Konsa', 'crest_villa', 'R', 'ENG', '23-10-1997', 'CB', 82, 183, 77, 'OF', 82, 68, 66, 80, 84, 42),
    ('P75', 'AV', 'Pau Torres', 'crest_villa', 'L', 'ESP', '16-01-1997', 'CB', 84, 191, 80, 'OF', 72, 80, 70, 78, 84, 48),
    # --- Newcastle United ---
    ('P76', 'NE', 'Nick Pope', 'crest_newcastle', 'R', 'ENG', '19-04-1992', 'GK', 84, 198, 90, 'GK', 84, 86, 82, 84, 48, 72),
    ('P77', 'NE', 'Dan Burn', 'crest_newcastle', 'L', 'ENG', '09-05-1992', 'CB', 80, 201, 92, 'OF', 58, 66, 56, 88, 82, 42),
    ('P78', 'NE', 'Sandro Tonali', 'crest_newcastle', 'R', 'ITA', '08-05-2000', 'CM', 85, 181, 78, 'OF', 78, 84, 82, 80, 78, 74),
    ('P79', 'NE', 'Joelinton', 'crest_newcastle', 'R', 'BRA', '14-08-1996', 'CM', 82, 186, 81, 'OF', 78, 76, 80, 88, 76, 74),
    # --- Coventry City ---
    ('P80', 'CO', 'Victor Lindelöf', 'crest_coventry', 'R', 'SWE', '17-07-1994', 'CB', 78, 187, 80, 'OF', 68, 72, 66, 76, 80, 42),
    ('P81', 'CP', 'Daniel Muñoz', 'crest_palace', 'R', 'COL', '26-05-1996', 'RB', 80, 180, 76, 'OF', 84, 70, 74, 82, 78, 62),
    ('P82', 'CP', 'Adam Wharton', 'crest_palace', 'R', 'ENG', '06-02-2004', 'CM', 80, 182, 72, 'OF', 72, 82, 80, 70, 72, 68),
    ('P83', 'CO', 'Haji Wright', 'crest_coventry', 'R', 'USA', '27-03-1998', 'ST', 74, 191, 84, 'OF', 78, 58, 70, 80, 34, 76),
    # --- Fulham FC ---
    ('P84', 'FU', 'Bernd Leno', 'crest_fulham', 'R', 'GER', '04-03-1992', 'GK', 84, 190, 83, 'GK', 84, 86, 82, 82, 56, 76),
    ('P85', 'FU', 'Antonee Robinson', 'crest_fulham', 'L', 'USA', '08-08-1997', 'LB', 82, 183, 73, 'OF', 90, 74, 76, 76, 76, 58),
    ('P86', 'FU', 'Alex Iwobi', 'crest_fulham', 'R', 'NGA', '14-05-1996', 'CM', 80, 180, 75, 'OF', 80, 80, 82, 70, 58, 72),
    ('P87', 'FU', 'Emile Smith Rowe', 'crest_fulham', 'R', 'ENG', '28-07-2000', 'CAM', 78, 182, 72, 'OF', 80, 78, 82, 62, 42, 74),
    # --- Ipswich Town ---
    ('P88', 'IP', 'Liam Delap', 'crest_ipswich', 'R', 'ENG', '08-02-2003', 'ST', 78, 186, 83, 'OF', 84, 62, 74, 84, 36, 80),
    ('P89', 'IP', 'Omari Hutchinson', 'crest_ipswich', 'L', 'ENG', '30-10-2003', 'RW', 76, 174, 68, 'OF', 86, 70, 82, 60, 34, 72),
    ('P90', 'IP', 'Jørgen Strand Larsen', 'crest_ipswich', 'R', 'NOR', '06-02-2000', 'ST', 78, 193, 86, 'OF', 74, 62, 70, 84, 36, 80),
    # --- Nottingham Forest ---
    ('P91', 'NF', 'Matz Sels', 'crest_forest', 'R', 'BEL', '26-02-1992', 'GK', 82, 188, 84, 'GK', 82, 84, 78, 80, 50, 72),
    ('P92', 'NF', 'Neco Williams', 'crest_forest', 'R', 'WAL', '13-04-2001', 'RB', 78, 177, 70, 'OF', 86, 72, 76, 72, 74, 60),
    ('P93', 'NF', 'Murillo', 'crest_forest', 'L', 'BRA', '04-07-2002', 'CB', 82, 184, 78, 'OF', 82, 70, 72, 80, 82, 48),
    ('P94', 'NF', 'Elliot Anderson', 'crest_forest', 'R', 'ENG', '06-11-2002', 'CM', 78, 179, 72, 'OF', 78, 78, 80, 72, 68, 72),
    # --- Sunderland AFC ---
    ('P95', 'SU', 'Dan Ballard', 'crest_sunderland', 'R', 'NIR', '22-09-1999', 'CB', 76, 187, 82, 'OF', 68, 60, 56, 82, 78, 40),
    ('P96', 'SU', 'Omar Alderete', 'crest_sunderland', 'L', 'PAR', '26-12-1996', 'CB', 76, 188, 84, 'OF', 66, 62, 58, 82, 78, 42),
    ('P97', 'SU', 'Granit Xhaka', 'crest_sunderland', 'L', 'SUI', '27-09-1992', 'CM', 82, 185, 82, 'OF', 58, 84, 74, 84, 78, 72),
    ('P98', 'SU', 'Brian Brobbey', 'crest_sunderland', 'R', 'NED', '01-02-2002', 'ST', 78, 180, 82, 'OF', 86, 60, 76, 84, 34, 78),
    # --- Manchester United ---
    ('P99', 'MU', 'Senne Lammens', 'crest_man_united', 'R', 'BEL', '02-07-2002', 'GK', 76, 193, 85, 'GK', 76, 78, 74, 74, 50, 72),
]

# Fixture_ID, Home, Away, DateTime, Home_Score, Away_Score, GW, POTM, Status
FIXTURES: list[tuple] = [
    ('F01', 'AR', 'MU', '22-09-2024 16:30', 2, 2, 5, 'P01', 'Completed'),
    ('F02', 'LV', 'CH', '20-10-2024 16:30', 2, 1, 8, 'P04', 'Completed'),
    ('F03', 'MC', 'AR', '02-11-2024 15:00', 1, 2, 10, 'P01', 'Completed'),
    ('F04', 'TH', 'CH', '10-11-2024 14:00', 1, 4, 11, 'P05', 'Completed'),
    ('F05', 'NE', 'AV', '16-11-2024 17:30', 1, 1, 12, 'P11', 'Completed'),
    ('F06', 'BH', 'MC', '23-11-2024 15:00', 1, 3, 12, 'P16', 'Completed'),
    ('F07', 'MU', 'EV', '24-11-2024 14:00', 2, 0, 12, 'P03', 'Completed'),
    ('F08', 'CP', 'LV', '01-12-2024 16:30', 0, 2, 13, 'P18', 'Completed'),
    ('F09', 'BO', 'BR', '07-12-2024 15:00', 2, 1, 14, 'P10', 'Completed'),
    ('F10', 'NF', 'FU', '08-12-2024 14:00', 1, 0, 14, 'P13', 'Completed'),
]

# Player_ID, Fixture_ID, Goals, Assists, Minutes, YC, RC, Saves, Conceded
PLAYER_STATS: list[tuple] = [
    ('P01', 'F01', 1, 1, 90, 1, 0, 0, 0),
    ('P03', 'F01', 1, 0, 90, 0, 0, 0, 0),
    ('P02', 'F01', 0, 0, 90, 0, 0, 5, 2),
    ('P08', 'F01', 0, 0, 90, 0, 0, 4, 2),
    ('P04', 'F02', 1, 1, 90, 0, 0, 0, 0),
    ('P05', 'F02', 0, 1, 90, 1, 0, 0, 0),
    ('P06', 'F02', 1, 0, 85, 0, 0, 0, 0),
    ('P07', 'F02', 0, 0, 90, 0, 0, 4, 1),
    ('P16', 'F03', 1, 0, 90, 0, 0, 0, 0),
    ('P01', 'F03', 1, 1, 90, 0, 0, 0, 0),
    ('P29', 'F03', 1, 0, 80, 0, 0, 0, 0),
    ('P24', 'F03', 0, 1, 90, 0, 0, 0, 0),
    ('P05', 'F04', 2, 1, 90, 0, 0, 0, 0),
    ('P27', 'F04', 1, 1, 90, 0, 0, 0, 0),
    ('P22', 'F04', 1, 0, 78, 0, 0, 0, 0),
    ('P19', 'F04', 1, 0, 90, 0, 0, 0, 0),
    ('P11', 'F05', 0, 1, 90, 0, 0, 0, 0),
    ('P26', 'F05', 1, 0, 90, 0, 0, 0, 0),
    ('P09', 'F05', 1, 0, 80, 0, 0, 0, 0),
    ('P16', 'F06', 2, 0, 90, 0, 0, 0, 0),
    ('P28', 'F06', 1, 1, 90, 0, 0, 0, 0),
    ('P23', 'F06', 1, 0, 90, 0, 0, 0, 0),
    ('P03', 'F07', 1, 1, 90, 0, 0, 0, 0),
    ('P12', 'F07', 1, 0, 85, 0, 0, 0, 0),
    ('P21', 'F07', 0, 0, 90, 0, 0, 5, 2),
    ('P18', 'F08', 1, 1, 90, 0, 0, 0, 0),
    ('P06', 'F08', 1, 0, 90, 0, 0, 0, 0),
    ('P20', 'F08', 0, 0, 90, 0, 0, 0, 0),
    ('P10', 'F09', 1, 1, 90, 0, 0, 0, 0),
    ('P17', 'F09', 1, 0, 88, 0, 0, 0, 0),
    ('P30', 'F09', 1, 0, 90, 0, 0, 0, 0),
    ('P13', 'F10', 1, 0, 90, 0, 0, 0, 0),
    ('P25', 'F10', 0, 1, 90, 0, 0, 0, 0),
]

ACCOLADES: list[tuple[str, str, str]] = [
    ('A01', 'P01', 'England Player of the Year'),
    ('A02', 'P03', 'Premier League Playmaker of the Season'),
    ('A03', 'P04', "PFA Players' Player of the Year"),
    ('A04', 'P05', 'Premier League Young Player of the Season'),
    ('A05', 'P01', 'Premier League Player of the Month'),
    ('A06', 'P16', 'Premier League Golden Boot'),
    ('A07', 'P15', 'Premier League Golden Glove'),
    ('A08', 'P24', 'Premier League Player of the Season'),
    ('A09', 'P18', 'Bundesliga Player of the Season'),
    ('A10', 'P14', 'England Midfielder of the Year'),
]
