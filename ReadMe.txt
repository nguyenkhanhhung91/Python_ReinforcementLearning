Tic tac toe is an easy game that we can apply reinforcemence learning to create AI bot.

There are several well known ways we can create a bot for this game:

1- a rule based bot that we hard code how the bot should play their move. This bot can't lose in a 3x3 tic tac toe game tbh. 
Basically there is a way for anyone to never lose so we just code this way for the bot. This bot can never learn.

2- Minimax. This algorithm uses tree data structure to store game states. A score function uses current piece and its position to score game states. A check mate state is scored the highest. Then, we just use this tree to find the next best state for bot(max) and worse state for opposite player(min)
	I've skipped this algorithm because it is just a search problem after you brute force all possible game state. This bot doesn't learn either.

3- Qlearning (Q for Quality-reinforcemence learning). This algorithm also score game state and the next game states similar to minimax. However, it's not a brute force approach. Rather, the Q-values (action and state score) tables are updated after each game. The state/action Q-value is updated and memorized using an equation which includes parameter like learning rate, and epsilon (explore or exploit rate) 
Qlearning is off policy because it always chooses the argmax Q-value unless the epsilon has been decreased many times and it's time to explore (see code). We set this explore rate as parameter.


4-Sarsa is on policy because it will learn to be careful in an environment where exploration is costly, Q-learning will not, it just randomly explore after exploitation for quite sometimes without considering the cost. Sarsa can learn the value of the random policy while acting randomly


5-Qlearning can learn by changing q-value after a game. However, this kind of intelligence doesn't generalize like a neural network, it doesn't apply for unseen state. Another limitation is memory and computation increases exponentially as game state increases.
The neural network can estimate qvalues to unseen states because it doesn't need to visit every state-action pair to learn. They way it learns is by adjusting the weights and biases in the network. For example, it compares Q-value at time t with the reward that you've got at time t after having executed action a + the prediction of the best Q-value of your neural network at time t+1

6- All of the above are model free, which means the algorithm doesn't update the model of environment, it only update the value function and policy.
A model based RL learns both from direct experience with the environment and from simulated experience with a model, which entails that it builds and updates a model of the environment.