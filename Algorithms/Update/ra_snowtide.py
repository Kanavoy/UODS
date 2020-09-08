from random import choice, randrange, shuffle
import networkx as nx

def perform_update(graph, opts, agents):
    speaker = choice(agents[0])
    x_i = graph.values["opinion"][speaker]
    u_i = graph.values["uncertainty"][speaker]
    for listener in agents[1]:
        x_j = graph.values["opinion"][listener]
        u_j = graph.values["uncertainty"][listener]
        h_ij = min((x_i+u_i,x_j+u_j)) - max((x_i-u_i,x_j-u_j))
        if h_ij <= u_i:
            try:
                print('getting rid of speaker')
                graph.remove_edge(listener, speaker)
            except nx.exception.NetworkXError:
                print('networkXerror')
                try:
                    graph.remove_edge(speaker, listener)
                    print('getting rid of listener')
                except nx.exception.NetworkXError:
                    print('networkXerror')
            finally:
				potential_friends = [n for n in agents[1]]
				shuffle(potential_friends)
                for new_friend in potential_friends:
                    x_k = graph.values["opinion"][new_friend]
                    op_diff_nf = x_j - x_k
                    current_friends = list(graph.neighbors(listener))
                    if new_friend == listener or new_friend in current_friends:
                        print ('I already know this guy')
                        continue
                    if op_diff_nf >0.25 or op_diff_nf<-0.25:
                        print ('I dont like this guy')
                        continue
                    graph.add_edge(listener, new_friend)
                    print('I made a new friend')
                    break
            continue
        rel_a = (h_ij/u_i)-1
        mu = opts.update.mu
        graph.values["opinion"][listener] = x_j + mu * rel_a * (x_i-x_j)
        graph.values["uncertainty"][listener] = u_j + mu * rel_a * (u_i-u_j)