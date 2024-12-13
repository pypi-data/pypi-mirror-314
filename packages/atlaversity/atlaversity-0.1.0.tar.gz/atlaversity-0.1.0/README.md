# About The Project

Atlaversity is a study and teaching aid for Atlantis PBEM currently targeting New Origins, https://atlantis-pbem.com/

# How to use

In order to use the project, there are a number of configuration and data files that needs to be present.

## atlaversity.toml

This is the main configuration file. It contains two configuration data fields:

- start_turn - This is the current turn number of the mages and study data files. This value needs to be stepped up for each turn. The data type for the field is Integer, e.g. start_turn = 20
- factions - A list of faction number for the factions who's mages' studies are being edited. The data type for the field is list of Integers, e.g. factions = [42, 62]

## mages CSVs

For each faction, there needs to be a CSV, Comma Separated Value, file called <code>mages<faction#><turn#>.csv</code>, e.g. <code>mages6220.csv</code>. This turn should be in a form that can be exported by Atlantis Little Helper, see https://atlantis-pbem.com/game-client.
When mages CSVs are exported from ALH, it needs to have the following settings:

- Separator: ,
- Format: days
- Orientation: Vertical

## mages-plan.csv

This is the actual study data file. It can be read from and written to by the application.
The file consist of three header rows and the rest are data rows

### Header rows

The first header row contains the IDs of all the mages for all factions. The list of IDs needs to match the combined list of mages for all mages CSVs and in the same order.
If the mages files for faction 42 and 62 contains the mages (456, 457) and (687, 789, 799) respectively, the first row of the mages-plan.csv file needs to be
<code>456,457,687,789,799</code>

The second header row contains the matching names for all the mages, preceeded by a '#'. The names does not need to match what the mages are actually called in the game. E.g.
<code>#Five of Ten,Nine of Eight,Three of Five,Seven of One,Four of Two</code>

The third header row contains a comment field for each mage, preceeded by a '#'. It was implemented to help remind what each mage should be focusing on. E.g.
<code>#ARTI,ARTI,ARTI,DRAG,DRAG</code>

### Data rows

Each row of data is either a comment row or a turn row. Comment rows are preceeded by a '#'.
Each turn row must contain a comma separated list of the orders for all mages. Orders can be

- A skill to study (four letter abbreviation). E.g. FORC, ESWO or DRAG
- If the mage should be teaching, the word TEACH plus trailing information about zero or more mages that are not to be taught. E.g.
  - TEACH (teaching with no exclusion)
  - TEACH-901-1205 (teaching, but not unit# 901 and 1205)
- An empty string if no study order have been set yet.

An example of an turn row could be:
FORC,PATT,DRAG,TEACH,FORC,ESWO,TEACH-901

A comment row can contain any data after the '#'. When a new mages-plan.csv file is saved, all comments are carried over to the new file.

# Example files

## atlaversity.toml

<code>start_turn = 21
factions = [47, 62]</code>

## mages4721.csv

<code>Skill,901 Rhydian Kweo,4560 Micaksica,6520 Count Borzoi,6521 Nashobah
BIRD,90,0,0,0
COMB,180,0,0,0
EART,90,65,60,0
FIRE,60,0,0,0
FORC,155,165,120,120
GATE,30,0,0,0
NECR,30,0,0,0
OBSE,65,0,0,0
PATT,175,120,150,135
SPIR,55,0,0,60
SUSK,30,0,0,0
WOLF,120,0,0,0</code>

## mages6221.csv

<code>Skill,916 Five of Ten,1656 Nine of Eight,1657 Three of Five,1658 Seven of One,1659 Four of Two
BIRD,60,120,60,120,120
COMB,180,0,0,0,0
EART,120,150,180,180,195
ESHI,60,0,0,0,0
FIRE,70,90,90,90,90
FORC,200,205,190,190,190
GATE,30,0,0,0,0
ILLU,105,90,90,90,75
OBSE,35,0,0,0,0
PATT,180,195,225,195,190
PHEN,30,40,40,40,30
SPIR,30,0,0,0,0
WOLF,90,120,60,30,90</code>

## mages-plan.csv

<code>901,4560,6520,6521,916,1656,1657,1658,1659
#Rhydian Kweo,Micaksica,Count Borzoi,Nashobah,Five of Ten,Nine of Eight,Three of Five,Seven of One,Four of Two
#DRAG,DRAG,DRAG,ARTI,DRAG,DRAG,DRAG,DRAG,DRAG
FORC,EART,EART,ARTI,ILLU,EART,BIRD,TEACH,WOLF
#This is a comment</code>
