A = readtable("./data/video1/keyframes_fourthpass_best.txt");
xvec = A.Var2;
yvec = A.Var3;
zvec = A.Var4;
figure();
scatter3(xvec,yvec,zvec);