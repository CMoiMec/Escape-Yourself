#coeff correspond à la puissance de 10 que l'on veut arrondir au dessus
def my_round(num,coeff):
    return (num//(10**coeff)+1)*(10**coeff)
