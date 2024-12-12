def expected_Hstrain_functions_fcc_1():
    R"""
    ** Branch 0 **
    ** 0 of 1 Orbits **  Points: 0  Mult: 1  MinLength: 0.00000  MaxLength: 0.00000
        Prototype of 1 Equivalent Clusters in Orbit 0
            Coordinates:
        Prototype basis functions:
            x \Phi_{0} = 1

            x \Phi_{1} = \sqrt{1/3}(E_1+E_2+E_3)

            x \Phi_{2} = \sqrt{1/3}(E_1^{2} +E_2^{2} +E_3^{2} )
            x \Phi_{3} = \sqrt{2/3}(E_1E_2+E_1E_3+E_2E_3)
            x \Phi_{4} = \sqrt{1/3}(E_4^{2} +E_5^{2} +E_6^{2} )

            x \Phi_{5} = \sqrt{1/3}(E_1^{3} +E_2^{3} +E_3^{3} )
            x \Phi_{6} = \sqrt{1/2}(E_1^{2} E_2+E_1^{2} E_3+E_1E_2^{2} +E_1E_3^{2} +
                         E_2^{2} E_3+E_2E_3^{2} )
            x \Phi_{7} = \sqrt{6}E_1E_2E_3
            x \Phi_{8} = (E_1E_4^{2} +E_2E_5^{2} +E_3E_6^{2} )
            x \Phi_{9} = \sqrt{1/2}(E_1E_5^{2} +E_1E_6^{2} +E_2E_4^{2} +E_2E_6^{2} +
                         E_3E_4^{2} +E_3E_5^{2} )
            x \Phi_{10} = \sqrt{6}E_4E_5E_6

    """
    return [
        {
            "coeff_coords": [[0], [1], [2]],
            "coeff_data": [0.5773502691896258, 0.5773502691896258, 0.5773502691896257],
        },
        {
            "coeff_coords": [[0, 0], [1, 1], [2, 2]],
            "coeff_data": [0.5773502691896261, 0.5773502691896261, 0.5773502691896253],
        },
        {
            "coeff_coords": [[0, 1], [0, 2], [1, 2]],
            "coeff_data": [0.8164965809277264, 0.816496580927726, 0.8164965809277258],
        },
        {
            "coeff_coords": [[3, 3], [4, 4], [5, 5]],
            "coeff_data": [0.5773502691896256, 0.5773502691896256, 0.577350269189626],
        },
        {"coeff_coords": [[0, 1, 2]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[3, 4, 5]], "coeff_data": [2.4494897427831783]},
        {
            "coeff_coords": [[0, 0, 0], [1, 1, 1], [2, 2, 2]],
            "coeff_data": [0.5773502691896261, 0.5773502691896261, 0.5773502691896251],
        },
        {
            "coeff_coords": [[0, 3, 3], [1, 4, 4], [2, 5, 5]],
            "coeff_data": [1.0, 1.0, 1.0000000000000002],
        },
        {
            "coeff_coords": [
                [0, 0, 1],
                [0, 0, 2],
                [0, 1, 1],
                [0, 2, 2],
                [1, 1, 2],
                [1, 2, 2],
            ],
            "coeff_data": [
                0.707106781186548,
                0.7071067811865477,
                0.707106781186548,
                0.7071067811865472,
                0.7071067811865475,
                0.7071067811865469,
            ],
        },
        {
            "coeff_coords": [
                [0, 4, 4],
                [0, 5, 5],
                [1, 3, 3],
                [1, 5, 5],
                [2, 3, 3],
                [2, 4, 4],
            ],
            "coeff_data": [
                0.7071067811865475,
                0.7071067811865481,
                0.7071067811865475,
                0.7071067811865481,
                0.7071067811865472,
                0.7071067811865469,
            ],
        },
    ]


def expected_Hstrain_functions_hcp_1():
    R"""
    ** Branch 0 **
    ** 0 of 1 Orbits **  Points: 0  Mult: 1  MinLength: 0.00000  MaxLength: 0.00000
        Prototype of 1 Equivalent Clusters in Orbit 0
            Coordinates:
        Prototype basis functions:
            x \Phi_{0} = 1

            x \Phi_{1} = \sqrt{1/2}(E_1+E_2)
            x \Phi_{2} = E_3

            x \Phi_{3} = \sqrt{3/8}(E_1^{2} +2/3E_1E_2+E_2^{2} +2/3E_6^{2} )
            x \Phi_{4} = \sqrt{4/3}(E_1E_2-1/2E_6^{2} )
            x \Phi_{5} = (E_1E_3+E_2E_3)
            x \Phi_{6} = E_3^{2}
            x \Phi_{7} = \sqrt{1/2}(E_4^{2} +E_5^{2} )

            x \Phi_{8} = \sqrt{11/32}(E_1^{3} +3/11E_1^{2} E_2+9/11E_1E_2^{2} +
                         6/11E_1E_6^{2} +9/11E_2^{3} +18/11E_2E_6^{2} )
            x \Phi_{9} = 1.25227(E_1^{2} E_2+14/23E_1E_2^{2} +2/23E_1E_6^{2} +
                         3/23E_2^{3} -16/23E_2E_6^{2} )
            x \Phi_{10} = \sqrt{18/23}(E_1E_2^{2} -3/2E_1E_6^{2} -1/3E_2^{3} +
                          1/2E_2E_6^{2} )
            x \Phi_{11} = \sqrt{9/8}(E_1^{2} E_3+2/3E_1E_2E_3+E_2^{2} E_3+
                          2/3E_3E_6^{2} )
            x \Phi_{12} = 2(E_1E_2E_3-1/2E_3E_6^{2} )
            x \Phi_{13} = \sqrt{3/2}(E_1E_3^{2} +E_2E_3^{2} )
            x \Phi_{14} = E_3^{3}
            x \Phi_{15} = \sqrt{9/8}(E_1E_4^{2} +1/3E_1E_5^{2} +1/3E_2E_4^{2} +
                          E_2E_5^{2} -\sqrt{8/9}E_4E_5E_6)
            x \Phi_{16} = (E_1E_5^{2} +E_2E_4^{2} +\sqrt{2}E_4E_5E_6)
            x \Phi_{17} = \sqrt{3/2}(E_3E_4^{2} +E_3E_5^{2} )

    """
    return [
        {"coeff_coords": [[2]], "coeff_data": [1.0]},
        {
            "coeff_coords": [[0], [1]],
            "coeff_data": [0.7071067811865475, 0.7071067811865477],
        },
        {"coeff_coords": [[2, 2]], "coeff_data": [1.0]},
        {
            "coeff_coords": [[0, 1], [5, 5]],
            "coeff_data": [1.1547005383792515, -0.5773502691896257],
        },
        {
            "coeff_coords": [[0, 2], [1, 2]],
            "coeff_data": [0.9999999999999999, 1.0000000000000002],
        },
        {
            "coeff_coords": [[3, 3], [4, 4]],
            "coeff_data": [0.7071067811865477, 0.7071067811865476],
        },
        {
            "coeff_coords": [[0, 0], [0, 1], [1, 1], [5, 5]],
            "coeff_data": [
                0.6123724356957941,
                0.4082482904638629,
                0.612372435695795,
                0.4082482904638629,
            ],
        },
        {"coeff_coords": [[2, 2, 2]], "coeff_data": [1.0]},
        {
            "coeff_coords": [[0, 1, 2], [2, 5, 5]],
            "coeff_data": [2.0, -0.9999999999999999],
        },
        {
            "coeff_coords": [[0, 2, 2], [1, 2, 2]],
            "coeff_data": [1.2247448713915887, 1.2247448713915892],
        },
        {
            "coeff_coords": [[2, 3, 3], [2, 4, 4]],
            "coeff_data": [1.2247448713915892, 1.2247448713915887],
        },
        {
            "coeff_coords": [[0, 4, 4], [1, 3, 3], [3, 4, 5]],
            "coeff_data": [0.9999999999999994, 1.0000000000000009, 1.4142135623730951],
        },
        {
            "coeff_coords": [[0, 0, 2], [0, 1, 2], [1, 1, 2], [2, 5, 5]],
            "coeff_data": [
                1.0606601717798207,
                0.7071067811865474,
                1.0606601717798223,
                0.7071067811865474,
            ],
        },
        {
            "coeff_coords": [[0, 1, 1], [0, 5, 5], [1, 1, 1], [1, 5, 5]],
            "coeff_data": [
                0.884651736929383,
                -1.3269776053940736,
                -0.29488391230979466,
                0.4423258684646917,
            ],
        },
        {
            "coeff_coords": [[0, 0, 1], [0, 1, 1], [0, 5, 5], [1, 1, 1], [1, 5, 5]],
            "coeff_data": [
                1.2522706649050823,
                0.7622517090726593,
                0.10889310129609413,
                0.16333965194414138,
                -0.8711448103687537,
            ],
        },
        {
            "coeff_coords": [[0, 3, 3], [0, 4, 4], [1, 3, 3], [1, 4, 4], [3, 4, 5]],
            "coeff_data": [
                1.0606601717798214,
                0.3535533905932737,
                0.3535533905932739,
                1.0606601717798214,
                -1.0,
            ],
        },
        {
            "coeff_coords": [
                [0, 0, 0],
                [0, 0, 1],
                [0, 1, 1],
                [0, 5, 5],
                [1, 1, 1],
                [1, 5, 5],
            ],
            "coeff_data": [
                0.5863019699779282,
                0.15990053726670778,
                0.47970161180012355,
                0.31980107453341555,
                0.4797016118001241,
                0.9594032236002471,
            ],
        },
    ]


def expected_Hstrain_functions_lowsym_1():
    return [
        {"coeff_coords": [[0]], "coeff_data": [1.0]},
        {"coeff_coords": [[1]], "coeff_data": [1.0]},
        {"coeff_coords": [[2]], "coeff_data": [1.0]},
        {"coeff_coords": [[3]], "coeff_data": [1.0]},
        {"coeff_coords": [[4]], "coeff_data": [1.0]},
        {"coeff_coords": [[5]], "coeff_data": [1.0]},
        {"coeff_coords": [[0, 0]], "coeff_data": [1.0]},
        {"coeff_coords": [[0, 1]], "coeff_data": [1.4142135623730951]},
        {"coeff_coords": [[0, 2]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[0, 3]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[0, 4]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[0, 5]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[1, 1]], "coeff_data": [1.0]},
        {"coeff_coords": [[1, 2]], "coeff_data": [1.4142135623730951]},
        {"coeff_coords": [[1, 3]], "coeff_data": [1.4142135623730951]},
        {"coeff_coords": [[1, 4]], "coeff_data": [1.4142135623730951]},
        {"coeff_coords": [[1, 5]], "coeff_data": [1.4142135623730951]},
        {"coeff_coords": [[2, 2]], "coeff_data": [1.0]},
        {"coeff_coords": [[2, 3]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[2, 4]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[2, 5]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[3, 3]], "coeff_data": [1.0]},
        {"coeff_coords": [[3, 4]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[3, 5]], "coeff_data": [1.4142135623730951]},
        {"coeff_coords": [[4, 4]], "coeff_data": [1.0]},
        {"coeff_coords": [[4, 5]], "coeff_data": [1.414213562373095]},
        {"coeff_coords": [[5, 5]], "coeff_data": [1.0]},
        {"coeff_coords": [[0, 0, 0]], "coeff_data": [1.0]},
        {"coeff_coords": [[0, 0, 1]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[0, 0, 2]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[0, 0, 3]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[0, 0, 4]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[0, 0, 5]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[0, 1, 1]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[0, 1, 2]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[0, 1, 3]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[0, 1, 4]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[0, 1, 5]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[0, 2, 2]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[0, 2, 3]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[0, 2, 4]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[0, 2, 5]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[0, 3, 3]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[0, 3, 4]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[0, 3, 5]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[0, 4, 4]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[0, 4, 5]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[0, 5, 5]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[1, 1, 1]], "coeff_data": [1.0]},
        {"coeff_coords": [[1, 1, 2]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[1, 1, 3]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[1, 1, 4]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[1, 1, 5]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[1, 2, 2]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[1, 2, 3]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[1, 2, 4]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[1, 2, 5]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[1, 3, 3]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[1, 3, 4]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[1, 3, 5]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[1, 4, 4]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[1, 4, 5]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[1, 5, 5]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[2, 2, 2]], "coeff_data": [1.0]},
        {"coeff_coords": [[2, 2, 3]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[2, 2, 4]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[2, 2, 5]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[2, 3, 3]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[2, 3, 4]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[2, 3, 5]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[2, 4, 4]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[2, 4, 5]], "coeff_data": [2.4494897427831783]},
        {"coeff_coords": [[2, 5, 5]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[3, 3, 3]], "coeff_data": [1.0]},
        {"coeff_coords": [[3, 3, 4]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[3, 3, 5]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[3, 4, 4]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[3, 4, 5]], "coeff_data": [2.449489742783178]},
        {"coeff_coords": [[3, 5, 5]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[4, 4, 4]], "coeff_data": [1.0]},
        {"coeff_coords": [[4, 4, 5]], "coeff_data": [1.7320508075688772]},
        {"coeff_coords": [[4, 5, 5]], "coeff_data": [1.7320508075688774]},
        {"coeff_coords": [[5, 5, 5]], "coeff_data": [1.0]},
    ]
