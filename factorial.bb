clear Z;
incr Z;
clear i;
while n not 0 do
    incr i;
    /*----------------------------
    Z1 = Z
*/
    clear Z1;
    clear tmpZ;
    while Z not 0 do
        incr Z1;
        decr Z;
        incr tmpZ;
    end;
/*
    # We commented out below lines because we do not need to keep the value of Z
    #while tmpZ;
    #    incr Z;
    #    decr tmpZ;
    #end;
    #----------------------------
    # Z = Z1i;
*/
    clear Z;
    clear tmpZ1;
    while Z1 not 0 do
        clear tmpI;
        while i not 0 do
            incr Z;
            decr i;
            incr tmpI;
        end;
        decr Z1;
        incr tmpZ1;
        while tmpI not 0 do
            incr i;
            decr tmpI;
        end;
    end;
    while tmpZ1 not 0 do
        incr Z1;
        decr tmpZ1;
    end;
    while tmpI not 0 do
        incr i;
        decr tmpI;
    end;
    decr n;
end;