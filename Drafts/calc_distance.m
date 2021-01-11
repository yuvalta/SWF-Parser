function d = calc_distance(mu1,mu2,sigma1,sigma2)


d = norm(mu1 - mu2) + norm(sigma1 - sigma2);

end