#!/usr/bin/env bash

tmux new-session -d -s simulated_all '
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type integrated_hessians --train_interaction_model;
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type expected_hessians;
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type hessians;
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type hessians_times_inputs;
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type shapley_sampling;
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type contextual_decomposition;
python3 get_performance.py --dataset simulated_all --visible_devices 0 --interaction_type neural_interaction_detection;
read;
'

tmux new-session -d -s simulated_maximum '
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type integrated_hessians --train_interaction_model;
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type expected_hessians;
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type hessians;
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type hessians_times_inputs;
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type shapley_sampling;
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type contextual_decomposition;
python3 get_performance.py --dataset simulated_maximum --visible_devices 1 --interaction_type neural_interaction_detection;
read;
'

tmux new-session -d -s simulated_minimum '
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type integrated_hessians --train_interaction_model;
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type expected_hessians;
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type hessians;
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type hessians_times_inputs;
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type shapley_sampling;
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type contextual_decomposition;
python3 get_performance.py --dataset simulated_minimum --visible_devices 2 --interaction_type neural_interaction_detection;
read;
'

tmux new-session -d -s simulated_multiply '
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type integrated_hessians --train_interaction_model;
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type expected_hessians;
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type hessians;
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type hessians_times_inputs;
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type shapley_sampling;
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type contextual_decomposition;
python3 get_performance.py --dataset simulated_multiply --visible_devices 3 --interaction_type neural_interaction_detection;
read;
'

tmux new-session -d -s simulated_squaresum '
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type integrated_hessians --train_interaction_model;
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type expected_hessians;
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type hessians;
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type hessians_times_inputs;
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type shapley_sampling;
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type contextual_decomposition;
python3 get_performance.py --dataset simulated_squaresum --visible_devices 4 --interaction_type neural_interaction_detection;
read;
'
