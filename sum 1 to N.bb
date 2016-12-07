clear I;
clear sum;
clear tempI;
while N not 0 do
    incr I;
    while I not 0 do
        incr sum;
        incr tempI;
        decr I;
    end;
    while tempI not 0 do
        incr I;
        decr tempI;
    end;
decr N;
end;
