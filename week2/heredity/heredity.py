import csv
import itertools
import sys

PROBS = {

    # Unconditional probabilities for having gene
    "gene": {
        2: 0.01,
        1: 0.03,
        0: 0.96
    },

    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability
    "mutation": 0.01
}


def main():
    #TODO replace no_* lists with else statements
    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people
    }
    
    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):

                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    
    no_gene = []
    no_trait = []
    no_parents = []
    prob = []
    final_prob = 1
    
    # Figure out multually exclusive categories for persons based on function arguments
    for person in people:
        if person not in one_gene and person not in two_genes:
            no_gene.append(person)
        if person not in have_trait:
            no_trait.append(person)
        if people[person]['mother'] == None and people[person]['father'] == None:
            no_parents.append(person)
    
    # Loop through each person in people and calculate gene and trait probs
    # vars gene and trait will be used to locate correct prob from PROBS
    # collect 2 probs from each person (gene, trait) and append to prob list
    for person in people:
        gene = None
        trait = None
        
        # For persons w/o documented parents use pop. data
        if person in no_parents:
            if person in no_gene:
                gene = 0
                if person in no_trait:
                    trait = False
                elif person in have_trait:
                    trait = True    
            elif person in one_gene:
                gene = 1
                if person in no_trait:
                    trait = False
                elif person in have_trait:
                    trait = True
            elif person in two_genes:
                gene = 2
                if person in no_trait:
                    trait = False
                elif person in have_trait:
                    trait = True
            
            prob.append(PROBS["gene"][gene])
            prob.append(PROBS["trait"][gene][trait])            
        
        # For persons w/ parents, first determine parents genotype individually
        # then calculate probability of passing on the required alleles to
        # their offspring
        else:
            child_gene_prob = None
            maternal = {}
            paternal = {}
            if people[person]['mother'] in no_gene:
                maternal = {0:1 - PROBS["mutation"], 1:PROBS["mutation"]}
            if people[person]['mother'] in one_gene:
                maternal = {0:0.5, 1:0.5}
            if people[person]['mother'] in two_genes:
                maternal = {0:PROBS["mutation"], 1:1 - PROBS["mutation"]}
            if people[person]['father'] in no_gene:
                paternal = {0:1 - PROBS["mutation"], 1:PROBS["mutation"]}
            if people[person]['father'] in one_gene:
                paternal = {0:0.5, 1:0.5}
            if people[person]['father'] in two_genes:
                paternal = {0:PROBS["mutation"], 1:1 - PROBS["mutation"]}
            
            if person in no_gene:
                child_gene_prob = (maternal[0] * paternal[0])
                gene = 0      
            if person in one_gene:
               child_gene_prob = (maternal[0] * paternal[1] + maternal[1] * paternal[0])
               gene = 1
            if person in two_genes:
                child_gene_prob = (maternal[1] * paternal[1])
                gene = 2        
            
            if person in no_trait:
                trait = False
            if person in have_trait:
                trait = True
                    
            prob.append(child_gene_prob)
            prob.append(PROBS["trait"][gene][trait])
    
    
    #Once all probs are collect calculate joint prob multipling each one        
    for value in prob:
        final_prob = final_prob * value
    
    return(final_prob)
            

def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    
    no_gene = []
    no_trait = []
    
    
    # Figure out multually exclusive categories for persons based on function arguments
    for person in probabilities:
        if person not in one_gene and person not in two_genes:
            no_gene.append(person)
        if person not in have_trait:
            no_trait.append(person)
    
    # Loop through catergories for each person, assigning num values
    # numerical vars gene & trait
    for person in probabilities:
        gene = None
        trait = None
        if person in no_gene:
            gene = 0
            if person in no_trait:
                trait = False
            elif person in have_trait:
                trait = True    
        elif person in one_gene:
            gene = 1
            if person in no_trait:
                trait = False
            elif person in have_trait:
                trait = True
        elif person in two_genes:
            gene = 2
            if person in no_trait:
                trait = False
            elif person in have_trait:
                trait = True
        
        # Update probabilities dict    
        probabilities[person]["gene"][gene] += p
        probabilities[person]["trait"][trait] += p


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    
    # Calulate total prob for all values in gene and trait
    for person in probabilities:
        gene_total = probabilities[person]["gene"][0] + probabilities[person]["gene"][1] + probabilities[person]["gene"][2]
        trait_total = probabilities[person]["trait"][False] + probabilities[person]["trait"][True]
        
        for i in [0, 1, 2]:
            probabilities[person]["gene"][i] = probabilities[person]["gene"][i] / gene_total
        for j in [False, True]:
            probabilities[person]["trait"][j] = probabilities[person]["trait"][j] / trait_total     


if __name__ == "__main__":
    main()
