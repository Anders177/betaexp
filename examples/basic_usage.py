from betaexp import BetaExpansion


system = BetaExpansion("1.7", precision=60)
digits = system.greedy("0.4", n_digits=20)
approximation = system.project(digits)

print("beta:", system.beta)
print("digits:", digits)
print("projection of the prefix:", approximation)
