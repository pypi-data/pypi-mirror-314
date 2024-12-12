from make_test_data import create_test_data
from hmm_functions import TrainModel, DecodeModel, HMMParam, read_HMM_parameters_from_file
from helper_functions import Load_observations_weights_mutrates

# -----------------------------------------------------------------------------
# Test data from quick tutorial
# -----------------------------------------------------------------------------

# Initial HMM guess
initial_hmm_params = HMMParam(state_names = ['Human', 'Archaic'], 
                              starting_probabilities = [0.5, 0.5], 
                              transitions = [[0.99,0.01],[0.02,0.98]], 
                              emissions = [0.03, 0.3]) 

# Create test data
obs, chroms, starts, variants, mutrates, weights  = create_test_data(50000, write_out_files = False)

# Train model
hmm_parameters = TrainModel(obs, mutrates, weights, initial_hmm_params)

# Decode model
segments = DecodeModel(obs, chroms, starts, variants, mutrates, weights, hmm_parameters)

for segment_info in segments:
    chrom, genome_start, genome_end, genome_length, state, mean_prob, snp_counter, ploidity, called_sequence, average_mutation_rate, variants = segment_info
    print(chrom, genome_start,  genome_end, genome_length, state, mean_prob, snp_counter, sep = '\t')

