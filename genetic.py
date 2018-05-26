import sys
import random
import nltk
import types
import time
from random import seed

name_seed = 0
#seed(37)
pop_size = 0
patterns = ''

''' TODO:
    Improve fitness function
        Decrease likelihood of converging on repeating words
        Get pattern match to actually do something useful
    Improve Speed
        should be able to handle large datasets 
'''
class Citizen: 
    def __init__(self, vocab, average):
        self.genes = []
        self.vocab = vocab
        self.average = average
        self.parents = []
        self.gene_parents = []
        self.name = 0
        self.fitness = 0
        self.select_prob = 0
        self.phenotype = ''
        self.grammar = ''
        
    def set_fitness(self):
        self.grammar = self.check_grammar()
        parse_grammar(self.vocab)
        grammar_eval = 2    
        if(self.grammar in patterns):
            grammar_eval = 20
        if(len(self.genes) == 1):
            grammar_eval = 1
        self.fitness = grammar_eval      
    
    def set_parent_genes(self):
        max_title_len = int(round(self.average+(0.2*self.average)))
        size = random.randint(1, max_title_len)
        for i in range(0, size):    
            index = random.randint(0, len(self.vocab)-1)
            chosen_gene = list(self.vocab.keys())[index]
            self.genes.append(chosen_gene)
            self.phenotype += ' ' + chosen_gene
            
    def set_genes(self, parents, size):
        for i in range(0, size):    
            parent_index = random.randint(0, len(parents)-1)
            parent = parents[parent_index]
            length_pgenes = len(parent.genes)
            gene_index = random.randint(0, length_pgenes-1)
            chosen_gene = parent.genes[gene_index]
            self.genes.append(chosen_gene)
            self.gene_parents.append(parent.name)  
            if(i > 1):
                mutate = random.uniform(0.0,1.0)
                self.mutation(mutate)           
        for gene in self.genes:
            self.phenotype += ' ' + gene
    
    def choose_parents(self, parents):
        max_title_len = int(round(self.average+(0.2*self.average)))
        size = random.randint(1, max_title_len)
        chosen = []
        num_parents = len(parents)
        for i in range(0,size):
            index = self.rank_selection(parents)
            chosen.append(parents[index])
        return chosen, size
    
    def rank_selection(self, parents):
        fit = []
        ranks = []
        weights = []
        current_rank = 0
        rank_index = 0
        for parent in parents:
            fit.append(parent.fitness)
        fit.sort()
        for rank in fit:
            if(rank != current_rank):
                current_rank = rank
                ranks.append(rank)
        max_rank = max(ranks)
        for rank in ranks:
            weight = 100 + (rank - max_rank)
            weights.append(weight)
        index = weighted_choice(weights)
        return index
                
    def check_grammar(self):
        word = nltk.tokenize.word_tokenize(self.phenotype)
        raw_pattern = nltk.pos_tag(word)
        pattern = [x[1] for x in raw_pattern]
        return(pattern) 
        
    def mutation(self, mutate):
        if(mutate <= 0.45):
                num_genes = len(self.genes)
                mut_gene = random.randint(0,num_genes-1)
                index = random.randint(0, len(self.vocab)-1)
                mutie = list(self.vocab.keys())[index]
                self.genes[mut_gene] = mutie                
    
    def __str__(self):
        return "Name: {} \nGenes: {} \nFitness: {} \n".format(self.name, self.phenotype, self.fitness)
                                                                
def initial_pop(vocab, average):
    global pop_size
    pop_size = int(len(vocab)*0.45)
    citizens = [Citizen(vocab, average) for i in range(0,pop_size)]
    for citizen in citizens:
        global name_seed
        citizen.name = name_seed
        name_seed += 1
        citizen.set_fitness()
        citizen.select_prob = name_seed
        citizen.set_parent_genes()
    return citizens
    
def weighted_choice(weights):
    totals = []
    running_total = 0

    for w in weights:
        running_total += w
        totals.append(running_total)

    rnd = random.random() * running_total
    for i, total in enumerate(totals):
        if rnd < total:
            return i   
                 
def generate_children(parents, vocab, average):
        global name_seed
        children = [Citizen(vocab, average) for i in range(0, pop_size)]
        for child in children:
            chosen_parents, num_parents = child.choose_parents(parents)
            child.set_genes(chosen_parents, num_parents)                
            child.name = name_seed
            child.set_fitness() 
            name_seed += 1
        return children

def parse_grammar(vocab):
        global patterns
        num_sentences = len(vocab)
        patterns = []
        for sentence in vocab:
            tokens = nltk.tokenize.word_tokenize(sentence)
            pattern = nltk.pos_tag(tokens)
            raw_patterns = [x[1] for x in pattern]
            patterns.append(raw_patterns)
             
def calc_prob(child, children, pop_size):
    total = 0
    for i in range(0,pop_size):
        total += children[i].fitness
    return(child.fitness/total)

def run_evolution(iterations, vocab, average):
    for k in range(0, iterations):
        print("------------------Generation {}-------------------".format(k))
        if (k == 0):
            citizens = initial_pop(vocab, average)
        if( k > 0):
            citizens = children
        children = generate_children(citizens, vocab, average)
        print("--------------------Parents--------------------------")
        for citizen in citizens:
            print(citizen)
        print("--------------------Children------------------------------")
        for child in children:
            child.select_prob = calc_prob(child, children, pop_size)
            print(child)
    return children

def main():
    run_evolution(0, dict(), 0)
    
if __name__ == '__main__':
    main()
        
