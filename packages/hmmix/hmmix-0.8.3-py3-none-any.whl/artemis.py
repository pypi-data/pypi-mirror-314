import numpy as np
from numba import njit
import matplotlib.pyplot as plt
import sys

from hmm_functions import Hybrid_path, Emission_probs_poisson, Calculate_Posterior_probabillities, calculate_log
from make_test_data import simulate_path, set_seed

@njit
def Speed_up_likelihood(trans, emission):
    return calculate_log(trans * emission)

@njit
def Calculate_loglikelihood(path, emissions, starting_probabilities, transitions):

    loglikelihood = 0
    for i, state in enumerate(path):
        if i == 0:
            loglikelihood += Speed_up_likelihood(starting_probabilities[state], emissions[i,state])
        else:
            loglikelihood += Speed_up_likelihood(transitions[path[i-1], state], emissions[i,state])

    return loglikelihood

def scale_values(values):

    min_value = min(values)
    max_value = max(values)

    if max_value - min_value == 0:
        sys.exit('All your values are exactly the same - try increasing the window size!')

    scaled_values = [(x - min_value) / (max_value - min_value) for x in values]
    return scaled_values


def distance_to_line(x, y, intercept, slope):
    return abs((slope * x) - y + intercept) / np.sqrt(slope ** 2 + 1)


def compute_confusion_matrix(true_array, pred_array, states):

    n_states = len(states)
    confusion_matrix = np.zeros((n_states, n_states))

    for true, pred in zip(true_array, pred_array):
        confusion_matrix[true, pred] += 1

    confusion_matrix_as_list = np.asarray(confusion_matrix).reshape(-1)

    return confusion_matrix_as_list


# Simulate
# 1) from hmm parameters
# 2) from hmm parameters, obs, weights, mutationrates

# something like:
# combinations, counts = np.unique(a, return_counts=True, axis=0)



def Find_best_alpha(hmm_parameters, data_set_length, outfile, out_plot_file, iterations, START, END, STEPS, SEED):

    # Config
    np.random.seed(SEED)
    set_seed(SEED)

    
    best_alphas = []

    with open(outfile, 'w') as out:

        n_states = len(hmm_parameters.state_names)
        state_names = hmm_parameters.state_names
        state_transition_names = [f'{state_names[x]}_{state_names[y]}' for x in range(n_states) for y in range(n_states)]
        print('iteration', 'alpha', 'point_wise_accuracy', 'loglikelihood', '\t'.join(state_transition_names), sep = '\t', file = out)
        

        for iteration in range(iterations):
            print(f'doing iteration {iteration + 1}/{iterations}')

            # simulate data
            obs, mutrates, weights, path = simulate_path(data_set_length, 1, hmm_parameters, SEED + iteration)    
            
            emissions = Emission_probs_poisson(hmm_parameters.emissions, obs, weights, mutrates)
            posterior_probs = Calculate_Posterior_probabillities(emissions, hmm_parameters)
            logged_posterior_probs = np.log(posterior_probs.T)
            
            x_coordinates = []
            y_coordinates = []
            alphas = []

            for ALPHA in np.linspace(START, END, STEPS):
                
                decoded_path = Hybrid_path(emissions, hmm_parameters.starting_probabilities, hmm_parameters.transitions, logged_posterior_probs, ALPHA)
                loglikelihood = Calculate_loglikelihood(decoded_path, emissions, hmm_parameters.starting_probabilities, hmm_parameters.transitions)
                point_wise_accuracy = np.sum(path == decoded_path) / len(decoded_path)

                x_coordinates.append(point_wise_accuracy)
                y_coordinates.append(loglikelihood)
                alphas.append(ALPHA)

                confusion_list = compute_confusion_matrix(path, decoded_path, hmm_parameters.state_names)

                print(iteration, round(ALPHA, 3), round(point_wise_accuracy,6), round(loglikelihood,3), '\t'.join([str(x) for x in confusion_list]), sep = '\t', file = out)

                


            # Find best alpha values
            scaled_x_coordinates = scale_values(x_coordinates)
            scaled_y_coordinates = scale_values(y_coordinates)

            best_dist, best_alpha = np.inf, 0
            for (alpha, x, y) in zip(alphas, scaled_x_coordinates, scaled_y_coordinates):
                dist = distance_to_line(x, y, 0, 1)
                if dist < best_dist:
                    best_dist, best_alpha = dist, alpha
            best_alphas.append(best_alpha)
            
            # Plot values
            plt.plot(scaled_x_coordinates, scaled_y_coordinates, color="grey") 


    # overall best alpha
    average_best_alpha = round(np.mean(best_alphas),3)
    min_best_alpha = round(average_best_alpha - 1.96 * np.std(best_alphas) / np.sqrt(iterations), 3)
    max_best_alpha = round(average_best_alpha + 1.96 * np.std(best_alphas) / np.sqrt(iterations), 3)

    print('best alpha:', average_best_alpha)


    # add regression line
    plt.plot(np.linspace(0, 1, 101), np.linspace(0, 1, 101), '--', color="black")

    # Add labels and title
    plt.xlabel('Scaled Pointwise accuracy')
    plt.ylabel('Scaled Log joint probability')
    plt.title(f'Average best alpha = {average_best_alpha} (95% CI {min_best_alpha} - {max_best_alpha}) \n{iterations} iterations\nn={data_set_length} observatins\n\n{hmm_parameters}')
    
    # Display the plot
    plt.grid(True)  
    plt.savefig(out_plot_file, bbox_inches='tight', dpi = 1000)

    return best_alphas


