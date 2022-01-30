# Spinning carousel quantum memory

The aim of this project is to reproduce a quantum memory on the $5$-qubit QuTech device stardom. However, the approach we decided to follow is not implementable in the real hardware at the moment, since it requires intermediate measurement. We so decided to simulate the device specific using qiskit density matrix simulator.
The work is inspired by [this paper](https://www.nature.com/articles/nature14270) and [this other paper](https://arxiv.org/pdf/2102.06132.pdf). However, they missed the flow of the music!
Here we report the topology of stardom:
<p align="center">
<img src="images/stardom.png" alt="drawing" width="100"/>
</p>

## How the carousel works 

<p align="center">
<img src="images/spinning_carousel.jpg" alt="drawing" width="300"/>
</p>

Do you remember those old festivals in which you would mount your fiery horse, and spin around while your parents were watching you? Well, here we go again (but quantum)!
We have four mighty horses.
Each time you buy a ticket you and your friends can mount up to three horses, and after each time you switch horse. Just to make sure you don't hurt the horses' feelings. So, the pattern of the ridden horses is:
1. $0,1,2$
2. $1,2,3$
3. $2,3,1$
4. $3,1,0$

At the end of each ride the occupied horses make a neighing. The one ridden in the middle actually makes two neighings! You know, first he answers the horse in front of him, and then the horse behind him. The free horse instead stays silent.

To me and you, all the horse noises seams the same. Really the same! But not to Bob, our *Parity checker* (yes, parity checker is a specific horce racing term). He knows how to talk with horses, and by hearing a couple of neighings (those after a single ride) he is able to understand if one of the horses is in distress! However, Bob cannot stop the carousel. He will write down who is in distress, and give him an extra carrot that evening!
Furthermore, by keeping one of the horses silent Bob is always able to understand who is in distress! While it would be a mess to hear from all the horses.
Bob is good at understanding horses. But he is simple-minded, he need the help of his friend Agent to decode the pattern and understand who and how many carrots are needed!

So, what happens in a given ride is ($i$ is defined module 4):
1. The horses $i-1$, $i$, $i+1$ are mounted;
2. After the first ride $i$ calls, $i-1$ answers. Then $i$ calls again but $i+1$ answers. $i+2$ stays silent, since it has no mounters;
3. Bob writes down the horses' conversation: OK or NOT OK
4. The carousel restart, by changing places
At the end of the day, Agent decodes the (OK, NOT OK) sequence, and distribute the carrots accordingly. If the number of carrots received are the correct number we are all happy! 

<p align="center">
<img src="images/Carousel.jpg" alt="drawing" width="800"/>
</p>

**NOTICE**: no horses were hurted in this process

## The quantum math behind the carousel
The project workflow is the following:
- Encode a general state 
    $$|\psi\rangle= \frac{1}{2}\big[ (1+e^{i\theta})|0\rangle + (1-e^{i\theta}|1\rangle \big]$$ 
    in the device, using $4$ physical qubits
- Measure repeatedly the state of the inner qubit, performing parity checks on 3 of the logical qubits. The set of three physical qubits spin around
- Save every measure that occurred during the simulation.
- Use a machine learning model to infer $\theta$ after as much time as possible
- listen to fancy quasi-quantum music!

### Preparing the carousel: the encoding
We encode, as an example, the state:
$$|\psi\rangle= \frac{1}{\sqrt{2}}\big[ |0\rangle -i |1\rangle \big]$$ 
into the state 
$$|\psi\rangle= \frac{1}{\sqrt{2}}\big[ |00s00\rangle -i |11s11\rangle \big]$$ 
in which $s\in\{0, 1\}$ is not important after the encoding. Below we show the encoding circuit. Notice that in this example and discussion we are showing the algorithm for the bit-flip. However, in the repository also the phase-flip algorithm is present.

![Encoding](images/encoding.png "Encoding")

### Listen to the horses: the parity checks
Then we apply the parity checks, also called syndrome detection. We treat it as a "spinning" $3$ qubit code. This means that the parity checks, at a given step, will be on:
1. $q_0 q_1$, $q_1 q_3$.
2. $q_1 q_3$, $q_3 q_4$.
3. $q_3 q_4$, $q_4 q_0$.
4. $q_4 q_0$, $q_0 q_1$.
This spinning version of the $(3+1)$-qubit code increase our ability to correct the system with respect to a trivial $4$-qubit code. Indeed, we use only $3$ qubits at a given step. In that step, we may recognise an error BUT if a second error occurs in the $4^{th}$ qubit, even at the same time of the previous error, the new problem can be recognized in the next step! We are then able to correct up to $2$ errors instead of $1$, if the extra error occurs where we are not watching!
Below we report the table for the syndromes. The value 'n.a.' denotes a parity check that is not performed.

| $q_0q_1$  | $q_1q_3$ | $q_3q_4$ | $q_4q_0$ | Qubit with error |
|-----------|----------|----------|----------|------------------|
|  0        | 1        | n.a.     | n.a.     | $q_3$ |
|  1        | 0        | n.a.     | n.a.     | $q_0$ |
|  1        | 1        | n.a.     | n.a.     | $q_1$ |
|  n.a.     | 0        | 1        | n.a.     | $q_4$ |
|  n.a.     | 1        | 0        | n.a.     | $q_1$ |
|  n.a.     | 1        | 1        | n.a.     | $q_3$ |
|  n.a.     | n.a.     | 0        | 1        | $q_0$ |
|  n.a.     | n.a.     | 1        | 0        | $q_3$ |
|  n.a.     | n.a.     | 1        | 1        | $q_4$ |
|  1        | n.a.     | n.a.     | 0        | $q_1$ |
|  0        | n.a.     | n.a.     | 1        | $q_4$ |
|  1        | n.a.     | n.a.     | 1        | $q_0$ |

It may seem a little strange, but the figure will clarify it!
![Syndromes](images/syndrome_detect.png "Syndrome")

However, we stress that we don't do any classically controlled operation to update the results. It will be our machine learning model that, given the error pattern, will understand the correct **classical** post-processing!

### Decoding the sequence: machine learning agent