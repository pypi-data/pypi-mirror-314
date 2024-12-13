def test_func():
    local = {
        'input': {
            'a': 1,
            'b': 2
        }
    }
    exec("def handle(a,b):\n    return a+b, a*b\noutput=handle(**input)", local)
    out = local['output']
    if not isinstance(out, tuple):
        out = (out, )
    output = {}
    for idx, unique in enumerate(['c', 'd']):
        output[unique] = out[idx]
    print(output)