#Optimize for the worst case scenario
'''
    After having identified the worst case scenarios (those with the maximum death outcomes) we are going to optimize for them.
'''

if __name__ == '__main__':
    # read the worst-case scenarios
    selected = pd.read_csv("intermediate outputs/step4 - prim results - worst case scenarios.csv")
    scenarios = [Scenario(f"{index}", **row) for index, row in selected.iterrows()]

    # create the model
    dike_model, planning_steps = get_model_for_problem_formulation(6)

    ema_logging.log_to_stderr(ema_logging.INFO)


    # run the optimization code
    def optimize(scenario, nfe, model, epsilons):

        with MultiprocessingEvaluator(model) as evaluator:
            results = evaluator.optimize(nfe=nfe, searchover='levers',
                                         epsilons=epsilons,
                                         reference=scenario)
        return results

    #save the results
    results = []
    for scenario in scenarios:

        epsilons = [0.1, ] * len(dike_model.outcomes)

        res = optimize(scenario, 100000, dike_model, epsilons)

        res.to_csv("intermediate outputs/step5 - multi scenario optimization results/step5 - " + str(scenario.name) + " optimization results.csv")

        results.append(res)
