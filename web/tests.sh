#!/bin/bash

for branch in newreactor master; do
    git checkout $branch
    
    for kind in s; do
        for bsize in 4 128; do
            for concurrency in 1 2 5 10 25 50 100; do
                echo -n "examples/benchmark.py -$kind -c $concurrency -i 8192 -n 100 -b $bsize: "
                examples/benchmark.py -$kind -c $concurrency -i 8192 -n 100 -b $bsize 2> /dev/null | grep "Result:"
            done
            
            echo
        done
        
        for bsize in 512 1024 4096; do
            for concurrency in 1 2 5 10 25 50 100 1000; do
                echo -n "examples/benchmark.py -$kind -c $concurrency -i 8192 -n 1000 -b $bsize: "
                examples/benchmark.py -$kind -c $concurrency -i 8192 -n 1000 -b $bsize 2> /dev/null | grep "Result:"
            done
            
            echo
        done
    done
done

# Tests to re-run:
# examples/benchmark.py -e -c 1000 -i 8192 -n 10000 -b 1024 | grep "Result:" # Marrow
# examples/benchmark.py -s -c 50 -i 8192 -n 10000 -b 512 | grep "Result:" # Tornado

# for kind in e s; do for bsize in 4 128; do for concurrency in 1 2 5 10 25 50 100; do (examples/benchmark.py -$kind -c $concurrency -i 8192 -n 100 -b $bsize 2> /dev/null | grep "Result:") ; done ; echo ; done ; done
