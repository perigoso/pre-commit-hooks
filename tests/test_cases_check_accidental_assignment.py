# (test case name, expected result True=pass False=fail, extra arguments, input)

test_cases = [
    (
        'control', True, {'strict': True}, '''
    int a = 0;
''',
    ),

    (
        'strict', True, {'strict': False}, '''
    (a = 0) ? 1 : 2;
''',
    ),

    (
        'strict', False, {'strict': True}, '''
    (a = 0) ? 1 : 2;
''',
    ),

    (
        'skip-keyword', True, {}, '''
    dummy_keyword(a = 1);
''',
    ),

    (
        'skip-keyword', False, {'strict': True}, '''
    dummy_keyword(a = 1);
''',
    ),

    (
        'skip-keyword', True, {'strict': True, 'ignore_keywords': ['dummy_keyword']}, '''
    dummy_keyword(a = 1);
''',
    ),

    (
        'cpp-comment', True, {'strict': True},
        '''
int main(void)
{
    /*
     * if (inside comment = 1)
     *
     */
}
''',
    ),

    (
        'cpp-comment', True, {'strict': True},
        '''
    if (1 /* (inside comment = 1) */) {
    {
        /* code */
    }
''',
    ),

    (
        'cpp-comment', True, {'strict': True},
        '''
    if (1 /* (inside comment = 1)
    * )
    */
    ) {
    {
        /* code */
    }
''',
    ),

    (
        'cpp-comment', True, {},
        '''
    while ((((dummy() /*/ a = 1 /* comment inside = 1 */))))
    {
        /* code */
    }
''',
    ),

    (
        'c-comment', True, {},
        '''
    for (int i = 0; // comment = 1
    i < 10;
    i++)
    {
        /* code */
    }
''',
    ),

    (
        'c-comment', True, {},
        '''
    for (int i = 0; // ;a=1;) for(;comment = 1;)
    i < 10;
    i++)
    {
        /* code */
    }
''',
    ),

    (
        'c-comment', True, {},
        '''
//	if (1)
//	{
//		/* code */
//	}
''',
    ),

    (
        'c-comment', True, {},
        '''
    if (1 //
    )
    {
        /* code */
    }
''',
    ),

    (
        'if', True, {},
        '''
    if (1)
    {
        /* code */
    }
''',
    ),


    (
        'if', False, {},
        '''
    if (a = 1)
    {
        /* code */
    }
''',
    ),

    (
        'if', False, {},
        '''
    if(1 = dummy())
    {
        /* code */
    }
''',
    ),

    (
        'if', False, {},
        '''
    if ((((dummy() = 1))))
    {
        /* code */
    }
''',
    ),

    (
        'if', True, {},
        '''
    if((((1))))
    {
        /* code */
    }
''',
    ),

    (
        'for', True, {},
        '''
    for (int i = 0; i < 10; i++)
    {
        /* code */
    }
''',
    ),

    (
        'for', True, {},
        '''
    for(int i=0;i<10;i++)
    {
        /* code */
    }
''',
    ),

    (
        'for', False, {},
        '''
    for (size_t i = 0; (i = count); i = i + 1)
    {
        /* code */
    }
''',
    ),

    (
        'for', False, {},
        '''
    for (size_t i = 0; i = count; i = i + 1)
    {
        /* code */
    }
''',
    ),

    (
        'while', True, {},
        '''
    while (1)
    {
        /* code */
    }
''',
    ),

    (
        'while', False, {},
        '''
    while(1 = dummy())
    {
        /* code */
    }
''',
    ),

    (
        'while', False, {},
        '''
    while ((((dummy() = 1))))
    {
        /* code */
    }
''',
    ),

    (
        'return', True, {'strict': False},
        '''
    return (i = 10);
''',
    ),

    (
        'return', False, {'strict': True},
        '''
    return (i = 10);
''',
    ),

    (
        'return', False, {'strict': True},
        '''
    return ((i = 10
    ));
''',
    ),

    (
        'return', True, {'strict': True},
        '''
    return ((i == 10
    ));
''',
    ),


    (
        'string', False, {'strict': True},
        '''
    print(a = "Hello World = 10");
''',
    ),

    (
        'string', True, {},
        '''
    print(a = "Hello World = 10");
''',
    ),

    (
        'string', True, {'strict': True},
        '''
    print("Hello World = 10");
''',
    ),

    (
        'string', True, {'strict': True},
        '''
    " (Hello World = 10) "
''',
    ),

    (
        'line-breaks', False, {'strict': True},
        '''
    return ((i
=
10
test
));
''',
    ),

    (
        'operator ==', True, {'strict': True},
        '''
    if (Hello World == 10) "
''',
    ),

    (
        'operator !=', True, {'strict': True},
        '''
    if (Hello World != 10) "
''',
    ),

    (
        'operator >=', True, {'strict': True},
        '''
    if (Hello World >= 10) "
''',
    ),

    (
        'operator <=', True, {'strict': True},
        '''
    if (Hello World <= 10) "
''',
    ),

    (
        'operator =!', False, {'strict': True},
        '''
    if (Hello World =! 10) "
''',
    ),

    (
        'operator =>', False, {'strict': True},
        '''
    if (Hello World => 10) "
''',
    ),

    (
        'operator =<', False, {'strict': True},
        '''
    if (Hello World =< 10) "
''',
    ),

    (
        'operator +=', False, {'strict': True},
        '''
    if (Hello World += 10) "
''',
    ),

    (
        'operator -=', False, {'strict': True},
        '''
    if (Hello World -= 10) "
''',
    ),

    (
        'operator *=', False, {'strict': True},
        '''
    if (Hello World *= 10) "
''',
    ),

    (
        'operator /=', False, {'strict': True},
        '''
    if (Hello World /= 10) "
''',
    ),

    (
        'operator %=', False, {'strict': True},
        '''
    if (Hello World %= 10) "
''',
    ),


    (
        'operator <<=', False, {'strict': True},
        '''
    if (Hello World <<= 10) "
''',
    ),

    (
        'operator >>=', False, {'strict': True},
        '''
    if (Hello World >>= 10) "
''',
    ),

    (
        'operator &=', False, {'strict': True},
        '''
    if (Hello World &= 10) "
''',
    ),

    (
        'operator ^=', False, {'strict': True},
        '''
    if (Hello World ^= 10) "
''',
    ),

    (
        'operator |=', False, {'strict': True},
        '''
    if (Hello World |= 10) "
''',
    ),
]
