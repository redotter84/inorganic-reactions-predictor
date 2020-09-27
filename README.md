# Inorganic Reactions Predictor

Software for predicting the chemical properties of inorganic compounds, 2016–2017.

## Build instructions

__Requirements__: Python 3

1. Download code
2. Open the folder with the code in the command line
3. Install the requirements: `pip install -r requirements.txt`
4. Run `main.pyw`

## What is it

This software is designed to predict reactions of inorganic chemical compounds. It was originally implemented for a conference on chemistry.

You can enter one or more formulas in the text box `Compounds`, then click `Compute`. The possible reactions with these compounds as an input will appear in the left box. The reactions which can be used to product them will be in the right box.

If you double-click the reaction, you will see a window where you can calculate masses of compounds in this reaction. For example, for a reaction `2H2 + O2 -> 2H2O` you can calculate how much oxygen and hydrogen you need to get one gram of water.

## How is it working

There are some schemes in the chemistry which can be used to understand if compounds can react or not. For example, we know that almost every acid is reacting with almost every alkali.

Using these schemes you can find some examples for a given compound. For instance, if you are given `NaOH` (which is an alkali), you almost certainly know that it will react with any acid or some salts. The program "knows" it too and it will give you an example of acid given alkali is reacting with. Also there is a small database of unique reactions.

The type of compound (e.g. alkali, acid, salt) can be inferred by its formula with enough accuracy. So you don't have to tell the program a type of compound you want to explore.
