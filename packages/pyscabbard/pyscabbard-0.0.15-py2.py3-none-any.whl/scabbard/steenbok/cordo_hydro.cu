


// transfers Qwin on a node to node basis
__global__ void compute_static(float *hw, float *Z, float *Qwx, float *Qwy, unsigned char *BC) {

	// Getting the right IF
	int x = threadIdx.x + blockIdx.x * blockDim.x;
	int y = threadIdx.y + blockIdx.y * blockDim.y;
	int idx,adder;
	if(get_index(x, y, idx, adder, BC) == false) return;
	if(BC::can_out(BC[idx])) return;




	// float surface_idx = hw[idx] + Z[idx];

	// float weights[NNEIGHBOURS];

	// for(int j=0;j<NNEIGHBOURS;++j){
	// 	weights[j] = 0.;
	// }

	// float sumWeights = 0.;

	// while(sumWeights == 0.){

	// 	for(int j=0;j<NNEIGHBOURS;++j){

	// 		// idx of the neighbours
	// 		int nidx;
	// 		if(get_neighbour(idx, adder, j, nidx) == false) continue;
			
	// 		// calculating local weight (i.e. Sw * dy)
	// 		float tw = surface_idx - (hw[nidx] + Z[nidx]);

	// 		if(tw<0) continue; // aborting if higher neighbour
			
	// 		// finishing slope calc
	// 		tw *= DYS[j];
	// 		tw /= DXS[j];

	// 		// saving weight
	// 		weights[j] = tw;

	// 		// summing all of em'
	// 		sumWeights += tw;
	// 	}

	// 	if(sumWeights == 0.) {
	// 		hw[idx] += 0.0001;
	// 		surface_idx += 0.0001;
	// 	}


	// }

	// for(int j=0;j<NNEIGHBOURS;++j){
	// 	if(weights[j] <= 0) continue;
	// 	int nidx;
	// 	if(get_neighbour(idx, adder, j, nidx) == false) continue;
		
	// 	atomicAdd(&QwB[nidx], QwA[idx] * weights[j]/sumWeights);
	// }

}