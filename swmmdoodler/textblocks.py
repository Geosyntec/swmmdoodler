# dictionaries of SWMM lines/parameters to insert into a preexisting model
## simple = "gully storage"
## complex = "green infrastructure"

simple_restricted = {
    'junctions': (
        '{node}_r{num}     {invert_R:.3f}          0          0          0          0\n'
        '{node}_rJ{num}    {invert_rJ:.3f}          0          0          0          0\n'
    ),
    # !how are we computing dmax here? currently set to 1.5
    'storage': (
        '{node}_rGS{num}   {invert_rGS:.3f}        1.5      0         TABULAR    {node}_StreetStorage{num}                0        0        0       \n'
    ),
    # !using default lengths, default roughness
    'conduits': (
        '{node}_rCon{num}   {node}_r{num}     {node}_rGS{num}   10        0.005      0          {offset_rCon:.3f}          0          0\n'
        '{node}_rGully{num} {node}_rJ{num}    {node}       10        0.005      0          {offset_rGully:.3f}          0          0\n'
    ),
    # !using default crest height
    'outlets': (
        '{node}_rSO{num}   {node}_rGS{num}   {node}_rJ{num}    0          TABULAR/DEPTH   {node}_Rstrctrs{num}                 NO\n'
    ),
    # Will the simple case always use a dummy shape?
    'xsections': (
        '{node}_rCon{num}   CIRCULAR        2                0          0          0         1\n'
        '{node}_rGully{num} CIRCULAR        2                0          0          0         1\n'
    ),
    'coordinates': (
        '{node}_r{num}     {xcoord_R:.3f}          {ycoord_R:.3f}\n'
        '{node}_rJ{num}    {xcoord_rJ:.3f}          {ycoord_rJ:.3f}\n'
        '{node}_rGS{num}   {xcoord_rGS:.3f}          {ycoord_rGS:.3f}\n'
    ),
    'inflows': (
        '{node}_r{num}         FLOW             {node}_r_ts{num}      FLOW     1.0      1.0      0\n'
    ),
    'time_series': (
        '{node}_r_ts{num}      FILE "{node}r{num}.txt"\n;\n'
    ),
}


simple_unrestricted = {
    'junctions': (
        '{node}_U{num}     {invert_U:.3f}          0          0          0          0\n'
    ),
    'conduits': (
        '{node}_uJ{num}     {node}_U{num}     {node}       50        0.01       0          0          0          0\n'
    ),
    'xsections': (
        '{node}_uJ{num}     CIRCULAR        2                0          0          0         1\n'
    ),
    'coordinates': (
        '{node}_U{num}     {xcoord_U:.3f}          {ycoord_U:.3f}\n'
    ),
    'inflows': (
        '{node}_U{num}         FLOW             {node}_U_ts{num}      FLOW     1.0      1.0      0\n'
    ),
    'time_series': (
        '{node}_U_ts{num}      FILE "{node}U{num}.txt"\n;\n'
    ),
}



complex_restricted = {
    'junctions': (
        '{node}_R_nP{num}     {invert_R_nP:.3f}          {dmax_R_nP:.3f}         0          0          0\n'
        '{node}_R_P{num}      {invert_R_P:.3f}         {dmax_R_P:.3f}          0          0          0\n'
        '{node}_R_nB{num}     {invert_R_nB:.3f}          {dmax_R_nB:.3f}         0          0          0\n'
        '{node}_R_B{num}      {invert_R_B:.3f}         {dmax_R_B:.3f}          0          0          0\n'
        '{node}_R_nR{num}     {invert_R_nR:.3f}          {dmax_R_nR:.3f}         0          0          0\n'
        '{node}_R_r{num}      {invert_R_r:.3f}         {dmax_R_r:.3f}          0          0          0\n'
        '{node}_R_nC{num}     {invert_R_nC:.3f}          {dmax_R_nC:.3f}         0          0          0\n'
        '{node}_R_C{num}      {invert_R_C:.3f}         {dmax_R_C:.3f}          0          0          0\n'
        '{node}_R_No{num}     {invert_R_No:.3f}         {dmax_R_No:.3f}          0          0          0\n'
        '{node}_R_n0{num}     {invert_R_n0:.3f}          {dmax_R_n0:.3f}         0          0          0\n'
        '{node}_R_nOt{num}    {invert_R_nOt:.3f}          {dmax_R_nOt:.3f}          0          0          0\n'
    ),
    'storage': (
        '{node}_R_sP{num}     {invert_R_sP}       {dmax_R_sP}     0         FUNCTIONAL {scoeff_R_sP}     0         0        0        0        0.05\n'
        '{node}_R_sB{num}     {invert_R_sB}       {dmax_R_sB}     0         FUNCTIONAL {scoeff_R_sB}     0         0        0        0        0.05\n'
        '{node}_R_sR{num}     {invert_R_sR}       {dmax_R_sR}     0         FUNCTIONAL {scoeff_R_sR}     0         0        0        0        0\n'
        '{node}_R_sC{num}     {invert_R_sC}       {dmax_R_sC}     0         FUNCTIONAL {scoeff_R_sC}       0         0        0        0        0\n'
        '{node}_R_sG{num}     {invert_R_sG}       {dmax_R_sG}      0         TABULAR    {node}_StreetStorage{num}                0        0        0\n'

    ),
    'conduits': (
        '{node}_R_cOtP{num}   {node}_R_nP{num}     {node}_R_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_R_cInP{num}   {node}_R_P{num}      {node}_R_sP{num}     10         0.01       0          {dmax_R_sP}          0          0\n'
        '{node}_R_cOtB{num}   {node}_R_nB{num}     {node}_R_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_R_cInB{num}   {node}_R_B{num}      {node}_R_sB{num}     10         0.01       0          {dmax_R_sB}          0          0\n'
        '{node}_R_cOtR{num}   {node}_R_nR{num}     {node}_R_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_R_cInR{num}   {node}_R_r{num}      {node}_R_sR{num}     10         0.01       0          {dmax_R_sR}          0          0\n'
        '{node}_R_cOtC{num}   {node}_R_nC{num}     {node}_R_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_R_cInC{num}   {node}_R_C{num}      {node}_R_sC{num}     10         0.01       0          {dmax_R_sC}          0          0\n'
        '{node}_R_cIn0{num}   {node}_R_No{num}     {node}_R_n0{num}     10         0.01       0          0          0          0\n'
        '{node}_R_cOt0{num}   {node}_R_n0{num}     {node}_R_sG{num}     10         0.01       0          {dmax_R_sG}          0          0\n'
        '{node}_R_cOt{num}    {node}_R_nOt{num}    {node}       10        0.01       0          {node_dmax:.3f}          0          0\n'
    ),
    'weirs': (
        '{node}_R_wP{num}     {node}_R_sP{num}     {node}_R_sG{num}     TRAPEZOIDAL  0.95       3.33       NO       0        0\n'
        '{node}_R_wB{num}     {node}_R_sB{num}     {node}_R_sG{num}     TRAPEZOIDAL  2.0        3.33       NO       0        0\n'
        '{node}_R_wR{num}     {node}_R_sR{num}     {node}_R_sG{num}     TRAPEZOIDAL  0.25       3.33       NO       0        0\n'
        '{node}_R_wC{num}     {node}_R_sC{num}     {node}_R_sG{num}     TRAPEZOIDAL  6          3.33       NO       0        0\n'

    ),
    'outlets': (
        '{node}_R_oP{num}     {node}_R_sP{num}     {node}_R_nP{num}     0.2        FUNCTIONAL/DEPTH 0.19             0.5        NO\n'
        '{node}_R_oB{num}     {node}_R_sB{num}     {node}_R_nB{num}     0.2        FUNCTIONAL/DEPTH 0.26             0.5        NO\n'
        '{node}_R_oR{num}     {node}_R_sR{num}     {node}_R_nR{num}     0          FUNCTIONAL/DEPTH 0.22             0.5        NO\n'
        '{node}_R_oC{num}     {node}_R_sC{num}     {node}_R_nC{num}     0          FUNCTIONAL/DEPTH 0.06             0.5        NO\n'
        '{node}_R_oG{num}     {node}_R_sG{num}     {node}_R_nOt{num}    0          TABULAR/DEPTH   {node}_Rstrctrs{num}                 NO\n'

    ),
    'xsections': (
        '{node}_R_cOtP{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cInP{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cOtB{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cInB{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cOtR{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cInR{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cOtC{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cInC{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cIn0{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cOt0{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_R_cOt{num}    CIRCULAR     2                0          0          0          1\n'
        '{node}_R_wP{num}     TRAPEZOIDAL  4                4          4          4\n'
        '{node}_R_wB{num}     TRAPEZOIDAL  4                4          4          4\n'
        '{node}_R_wR{num}     TRAPEZOIDAL  4                4          4          4\n'
        '{node}_R_wC{num}     TRAPEZOIDAL  4                4          4          4\n'

    ),
    'coordinates': (
        '{node}_R_nP{num}      {xcoord_R_nP}      {ycoord_R_nP}\n'
        '{node}_R_P{num}      {xcoord_R_P}      {ycoord_R_P}\n'
        '{node}_R_nB{num}      {xcoord_R_nB}      {ycoord_R_nB}\n'
        '{node}_R_B{num}      {xcoord_R_B}      {ycoord_R_B}\n'
        '{node}_R_nR{num}      {xcoord_R_nR}      {ycoord_R_nR}\n'
        '{node}_R_r{num}      {xcoord_R_r}      {ycoord_R_r}\n'
        '{node}_R_nC{num}      {xcoord_R_nC}      {ycoord_R_nC}\n'
        '{node}_R_C{num}      {xcoord_R_C}      {ycoord_R_C}\n'
        '{node}_R_No{num}      {xcoord_R_No}      {ycoord_R_No}\n'
        '{node}_R_n0{num}      {xcoord_R_n0}      {ycoord_R_n0}\n'
        '{node}_R_nOt{num}      {xcoord_R_nOt}      {ycoord_R_nOt}\n'
        '{node}_R_sP{num}      {xcoord_R_sP}      {ycoord_R_sP}\n'
        '{node}_R_sB{num}      {xcoord_R_sB}      {ycoord_R_sB}\n'
        '{node}_R_sR{num}      {xcoord_R_sR}      {ycoord_R_sR}\n'
        '{node}_R_sC{num}      {xcoord_R_sC}      {ycoord_R_sC}\n'
        '{node}_R_sG{num}      {xcoord_R_sG}      {ycoord_R_sG}\n'
    ),
    'inflows': (
        '{node}_R_P{num}      FLOW             {node}r{num} FLOW     1.0      0.000\n'
        '{node}_R_B{num}      FLOW             {node}r{num} FLOW     1.0      0.000\n'
        '{node}_R_r{num}      FLOW             {node}r{num} FLOW     1.0      0.000\n'
        '{node}_R_C{num}      FLOW             {node}r{num} FLOW     1.0      0.000\n'
        '{node}_R_No{num}     FLOW             {node}r{num} FLOW     1.0      1.000\n'

    ),
    'time_series': (
        '{node}r{num}      FILE "{node}r{num}.txt"\n;\n'
        '{node}r{num}      FILE "{node}r{num}.txt"\n;\n'
        '{node}r{num}      FILE "{node}r{num}.txt"\n;\n'
        '{node}r{num}      FILE "{node}r{num}.txt"\n;\n'
        '{node}r{num}      FILE "{node}r{num}.txt"\n;\n'
    ),
}


complex_unrestricted = {
    'junctions': (
        '{node}_U_NoGI{num}   {invert_U_NoGI:.3f}          {dmax_U_NoGI:.3f}          0          0          0\n'
        '{node}_U_P{num}      {invert_U_P:.3f}          {dmax_U_P:.3f}          0          0          0\n'
        '{node}_U_B{num}      {invert_U_B:.3f}          {dmax_U_B:.3f}          0          0          0\n'
        '{node}_U_r{num}      {invert_U_r:.3f}          {dmax_U_r:.3f}          0          0          0\n'
        '{node}_U_C{num}      {invert_U_C:.3f}          {dmax_U_C:.3f}          0          0          0\n'
        '{node}_U_n0{num}     {invert_U_n0:.3f}          {dmax_U_n0:.3f}          0          0          0\n'
        '{node}_U_nP{num}     {invert_U_nP:.3f}          {dmax_U_nP:.3f}          0          0          0\n'
        '{node}_U_nB{num}     {invert_U_nB:.3f}          {dmax_U_nB:.3f}          0          0          0\n'
        '{node}_U_nR{num}     {invert_U_nR:.3f}          {dmax_U_nR:.3f}          0          0          0\n'
        '{node}_U_nC{num}     {invert_U_nC:.3f}          {dmax_U_nC:.3f}          0          0          0\n'
        '{node}_U_nOt{num}    {invert_U_nOt:.3f}          {dmax_U_nOt:.3f}          0          0          0\n'
    ),
    'storage': (
        '{node}_U_sP{num}     {invert_U_sP}       {dmax_U_sP}     0         FUNCTIONAL {scoeff_U_sP}     0         0        0        0        0.05\n'
        '{node}_U_sB{num}     {invert_U_sB}       {dmax_U_sB}     0         FUNCTIONAL {scoeff_U_sB}      0         0        0        0        0.05\n'
        '{node}_U_sR{num}     {invert_U_sR}       {dmax_U_sR}     0         FUNCTIONAL {scoeff_U_sR}     0         0        0        0        0\n'
        '{node}_U_sC{num}     {invert_U_sC}       {dmax_U_sC}     0         FUNCTIONAL {scoeff_U_sC}       0         0        0        0        0\n'

    ),
    'conduits': (
        '{node}_U_cIn0{num}   {node}_U_NoGI{num}   {node}_U_n0{num}     10         0.01       0          0          0          0\n'
        '{node}_U_cOt0{num}   {node}_U_n0{num}     {node}_U_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_U_cInP{num}   {node}_U_P{num}      {node}_U_sP{num}     10         0.01       0          {dmax_U_sP}          0          0\n'
        '{node}_U_cOtP{num}   {node}_U_nP{num}     {node}_U_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_U_cInB{num}   {node}_U_B{num}      {node}_U_sB{num}     10         0.01       0          {dmax_U_sB}          0          0\n'
        '{node}_U_cOtB{num}   {node}_U_nB{num}     {node}_U_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_U_cInR{num}   {node}_U_r{num}      {node}_U_sR{num}     10         0.01       0          {dmax_U_sR}          0          0\n'
        '{node}_U_cOtR{num}   {node}_U_nR{num}     {node}_U_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_U_cInC{num}   {node}_U_C{num}      {node}_U_sC{num}     10         0.01       0          {dmax_U_sC}          0          0\n'
        '{node}_U_cOtC{num}   {node}_U_nC{num}     {node}_U_nOt{num}    10         0.01       0          0          0          0\n'
        '{node}_U_cOt{num}    {node}_U_nOt{num}    {node}       10        0.01       0          {node_dmax:.3f}          0          0\n'
    ),
    'weirs': (
        '{node}_U_wP{num}     {node}_U_sP{num}     {node}_U_nP{num}     TRAPEZOIDAL  0.95       3.33       NO       0        0\n'
        '{node}_U_wB{num}     {node}_U_sB{num}     {node}_U_nB{num}     TRAPEZOIDAL  2.0        3.33       NO       0        0\n'
        '{node}_U_wR{num}     {node}_U_sR{num}     {node}_U_nR{num}     TRAPEZOIDAL  0.25       3.33       NO       0        0\n'
        '{node}_U_wC{num}     {node}_U_sC{num}     {node}_U_nC{num}     TRAPEZOIDAL  6          3.33       NO       0        0\n'

    ),
    'outlets': (
        '{node}_U_oP{num}     {node}_U_sP{num}     {node}_U_nP{num}     0.2        FUNCTIONAL/DEPTH 0.18             0.5        NO\n'
        '{node}_U_oB{num}     {node}_U_sB{num}     {node}_U_nB{num}     0.2        FUNCTIONAL/DEPTH 0.15             0.5        NO\n'
        '{node}_U_oR{num}     {node}_U_sR{num}     {node}_U_nR{num}     0          FUNCTIONAL/DEPTH 0.22             0.5        NO\n'
        '{node}_U_oC{num}     {node}_U_sC{num}     {node}_U_nC{num}     0          FUNCTIONAL/DEPTH 0.06             0.5        NO\n'

    ),
    'xsections': (
        '{node}_U_cIn0{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cOt0{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cInP{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cOtP{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cInB{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cOtB{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cInR{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cOtR{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cInC{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cOtC{num}   CIRCULAR     2                0          0          0          1\n'
        '{node}_U_cOt{num}    CIRCULAR     2                0          0          0          1\n'
        '{node}_U_wP{num}     TRAPEZOIDAL  4                3.71       4          4\n'
        '{node}_U_wB{num}     TRAPEZOIDAL  4                4.0        4          4\n'
        '{node}_U_wR{num}     TRAPEZOIDAL  4                1.38       4          4\n'
        '{node}_U_wC{num}     TRAPEZOIDAL  4                1.73       4          4\n'

    ),
    'coordinates': (
        '{node}_U_NoGI{num}      {xcoord_U_NoGI}      {ycoord_U_NoGI}\n'
        '{node}_U_P{num}      {xcoord_U_P}      {ycoord_U_P}\n'
        '{node}_U_B{num}      {xcoord_U_B}      {ycoord_U_B}\n'
        '{node}_U_r{num}      {xcoord_U_r}      {ycoord_U_r}\n'
        '{node}_U_C{num}      {xcoord_U_C}      {ycoord_U_C}\n'
        '{node}_U_n0{num}      {xcoord_U_n0}      {ycoord_U_n0}\n'
        '{node}_U_nP{num}      {xcoord_U_nP}      {ycoord_U_nP}\n'
        '{node}_U_nB{num}      {xcoord_U_nB}      {ycoord_U_nB}\n'
        '{node}_U_nR{num}      {xcoord_U_nR}      {ycoord_U_nR}\n'
        '{node}_U_nC{num}      {xcoord_U_nC}      {ycoord_U_nC}\n'
        '{node}_U_nOt{num}      {xcoord_U_nOt}      {ycoord_U_nOt}\n'
        '{node}_U_sP{num}      {xcoord_U_sP}      {ycoord_U_sP}\n'
        '{node}_U_sB{num}      {xcoord_U_sB}      {ycoord_U_sB}\n'
        '{node}_U_sR{num}      {xcoord_U_sR}      {ycoord_U_sR}\n'
        '{node}_U_sC{num}      {xcoord_U_sC}      {ycoord_U_sC}\n'
    ),
    'inflows': (
        '{node}_U_NoGI{num}   FLOW             {node}U{num} FLOW     1.0      1.000\n'
        '{node}_U_P{num}      FLOW             {node}U{num} FLOW     1.0      0.000\n'
        '{node}_U_B{num}      FLOW             {node}U{num} FLOW     1.0      0.000\n'
        '{node}_U_r{num}      FLOW             {node}U{num} FLOW     1.0      0.000\n'
        '{node}_U_C{num}      FLOW             {node}U{num} FLOW     1.0      0.000\n'

    ),
    'time_series': (
        '{node}U{num}      FILE "{node}U{num}.txt"\n;\n'
        '{node}U{num}      FILE "{node}U{num}.txt"\n;\n'
        '{node}U{num}      FILE "{node}U{num}.txt"\n;\n'
        '{node}U{num}      FILE "{node}U{num}.txt"\n;\n'
        '{node}U{num}      FILE "{node}U{num}.txt"\n;\n'
    ),
}
