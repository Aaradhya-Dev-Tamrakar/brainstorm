# Latexmk configuration for BiasAperture report
# Enables automatic processing of glossaries (acronyms and symbols)

add_cus_dep('glo', 'gls', 0, 'run_makeglossaries');
add_cus_dep('acn', 'acr', 0, 'run_makeglossaries');
add_cus_dep('slo', 'sls', 0, 'run_makeglossaries');

sub run_makeglossaries {
    system("makeglossaries", $_[0]);
    return 0;
}

push @generated_exts, 'glo', 'gls', 'glg';
push @generated_exts, 'acn', 'acr', 'alg';
push @generated_exts, 'slo', 'sls', 'slg';
