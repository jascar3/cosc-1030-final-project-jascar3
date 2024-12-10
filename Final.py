'''
# Information about Basketball and the situation we are handling

Basketball is a team sport played between two teams, each consisting of five players. The game takes place on a rectangular court, usually indoors.  It is a complex game, and we will need to make many assumptions to help with reducing the number of thing we need to program to a manageable level!  Consider the following information.  We will add to this and build some other support materials over the coming month (hopefully together in those new sync sessions!).


Here are the fundamental elements of basketball:

## Objective:

The primary goal is to score points by tossing the ball through the opponent’s goal, which is an elevated horizontal hoop and net called a basket.

## Scoring:

Two-Point Scenario: A two-pointer refers to a shot made from anywhere inside the three-point arc. Successful two-point shots add two points to the team’s total score. These shots can include jump shots, layups, and dunks.
Three-Point Scenario: Shots made from beyond the three-point arc count for three points.

## Fouls:

A foul occurs when a player violates the rules, often through illegal personal contact with an opponent or unsportsmanlike behavior.

## Free Throws:

After a foul, the clock stops while the fouled player shoots free throws.  While there are different situations in which a player might shoot one or two free throws for one point each, for our program, assume that the team that was fouled will always have the chance for two free throws.

## Time to advance the ball or to foul:  

It takes some time to advance the ball up the court to attempt a two point shot.  We will need to account for this.  It also takes some time (usually a bit less) to commit a foul to stop the clock.
'''

# Game parameters
three_point_percentage = 0.35  # 35% chance of making a 3-pointer
two_point_percentage = 0.45  # 45% chance of making a 2-pointer
free_throw_percentage = 0.75  # 75% chance for opponent's free-throw success
offensive_rebound_probability = 0.3  # 30% chance of getting an offensive rebound
time_remaining = 30  # seconds left in the game
probability_of_overtime_win = 0.6  # 60% chance of winning in overtime

# Define player stats and game state
player_stats = {
    "three_point_percentage": three_point_percentage,
    "two_point_percentage": two_point_percentage
}

opponent_free_throw_percentage = free_throw_percentage

# Simulation function
def run_simulation(team_score, opponent_score):
    current_time = time_remaining
    game_over = False

    # Check if team is down by 3 points and time remaining is 30 seconds
    if team_score < opponent_score - 3 and current_time <= 30:
        # Evaluate shot options: Hard 3-pointer or Easy 2-pointer
        shot_choice = evaluate_shot_options()

        if shot_choice == "Hard 3":
            game_over, team_score, current_time = take_hard_3(team_score, opponent_score, current_time)
        elif shot_choice == "Easy 2":
            game_over, team_score, current_time = take_easy_2(team_score, opponent_score, current_time)

    else:
        # If game is not in the critical state, end the simulation
        game_over = True

    # Final decision on game outcome after taking shot
    if not game_over:
        # Final game state and result
        if team_score >= opponent_score:
            return "Win", team_score, opponent_score
        else:
            return "Lose", team_score, opponent_score
    else:
        return "End", team_score, opponent_score

# Evaluate shot options: Hard 3-pointer vs Easy 2-pointer
def evaluate_shot_options():
    # Calculate expected outcomes for Hard 3-pointer and Easy 2-pointer
    hard_3_success_rate = player_stats["three_point_percentage"]
    easy_2_success_rate = player_stats["two_point_percentage"]

    # We assume a hard 3-pointer is more likely to tie, but with lower success
    if hard_3_success_rate > easy_2_success_rate:
        return "Hard 3"
    else:
        return "Easy 2"

# Simulate taking a hard 3-pointer
def take_hard_3(team_score, opponent_score, current_time):
    success = random.random() < player_stats["three_point_percentage"]
    if success:
        team_score += 3
    # Update time (we assume it takes 6 seconds to take the shot)
    current_time -= 6
    if current_time <= 0 or team_score == opponent_score:
        return True, team_score, current_time
    return False, team_score, current_time

# Simulate taking an easy 2-pointer
def take_easy_2(team_score, opponent_score, current_time):
    success = random.random() < player_stats["two_point_percentage"]
    if success:
        team_score += 2
    # Update time (we assume it takes 4 seconds to take the shot)
    current_time -= 4
    if current_time <= 0 or team_score == opponent_score:
        return True, team_score, current_time
    return False, team_score, current_time

# Simulate the outcome of multiple simulations (Monte Carlo)
def monte_carlo_simulation(num_simulations, initial_team_score, initial_opponent_score):
    results = {"Win": 0, "Lose": 0, "End": 0}
    for _ in range(num_simulations):
        result, final_team_score, final_opponent_score = run_simulation(initial_team_score, initial_opponent_score)
        results[result] += 1
    win_percentage = (results["Win"] / num_simulations) * 100
    lose_percentage = (results["Lose"] / num_simulations) * 100
    return win_percentage, lose_percentage, results

# Example simulation run
initial_team_score = 90
initial_opponent_score = 93
num_simulations = 10000

win_percentage, lose_percentage, results = monte_carlo_simulation(num_simulations, initial_team_score, initial_opponent_score)

print(f"Win Percentage: {win_percentage}%")
print(f"Lose Percentage: {lose_percentage}%")
print(f"Results: {results}")