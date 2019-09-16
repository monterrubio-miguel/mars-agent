# mars-explorer
All credit to https://github.com/mihneadb/mars-explorer. This repo is a modification of mihneadb's. Made for a school assignment

## Run me

```bash
python main.py --help
usage: main.py [-h] [--obstacles OBSTACLES] [--rocks ROCKS]
               [--explorers EXPLORERS] [--carriers CARRIERS] [--iscoop 0/1]

optional arguments:
  -h, --help            show this help message and exit
  --obstacles OBSTACLES
  --rocks ROCKS
  --explorers EXPLORERS
  --carriers CARRIERS
  --iscoop IS COOPERATIVE OR INDIVIDUAL (Note: Inputting any other option other than '1' will default to '0')

```

All params have defaults.

## Details

### Explorers

* can carry 1 rock
* know where the base is
* can sense nearby rocks
* can sense if they are "on" a rock or the base

## Modes

### Individual

Explorers wander about. When they find a rock, they pick it up and leave a trail of crumbs on their way back to the base. If another explorer finds this trail, it will follow it to the destination where the previous explorer had found a rock.

    To run in this mode, you need to pass `--iscoop false`.

<!-- ![demo-without-carriers](https://raw.githubusercontent.com/mihneadb/mars-explorer/master/demo-gifs/mars-explorer-no-carriers.gif)
 -->
### Cooperative (default)

Explorers wander about. When they find a rock, they pick it up and take it to the base.

<!-- ![demo-with-carriers](https://raw.githubusercontent.com/mihneadb/mars-explorer/master/demo-gifs/mars-explorer-carriers.gif)
 -->