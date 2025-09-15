# WFREQ is a tool for data analyzing


## DOCS

### At first to download a package with aur you can use

```yay -S wfreq```

#### It will install all needed packages and wfreq

### Then you can use it on your system with

```wfreq <data path> <another arguments>```

### You can also use some arguments for configure your output format and spec your analyzation stack:

#### -f | --frequent - to say how many frequent words to output(number)

#### -r | --rare - to say how many rare words to output(number)

#### -rf | --red_flags - to say which words not to contain in answer(word list | file | folder)(words should be organized through comma ,)




## Dev processes

### Steps of developing:

1. [x] Build MVP(Minimal Viable Project)

### Need to develop:

- [ ] API data recognizing
- [ ] Web pages analyzing
- [ ] Pattern searching
- [ ] Language analyze
- [ ] Morphologic validator
- [ ] Dictionaries
- [ ] Logging
- [ ] Centralized analyzation
- [ ] Word divide by type(noun, verb e.t.c)
- [ ] Smart analyze(patters, red flags, artifacts, languages, slang e.t.c.)
- [ ] ML integration

### Tech stack ideas:

#### Languages:

- Python(for everything on the start, then: ML, CLI visualizing e.t.c.)
- Rust(for algorithms in the future)
- Java and Swift(for wided apps)
