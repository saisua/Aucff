# Aucff
Custom file format

## Examples

Single integer
`i/123`

Single float
`f/123.456`

Single string
`s/Hello, world!`

Single boolean
`b/t`

Single list with consistent types
```
[s/
123
123.456
Hello, world!
t
]
```

Single list
```
[
    i/123
    f/123.456
    s/Hello, world!
    b/t
]
```

Single dictionary with consistent key types
```
{s/
    123: s/Hello, world!
    hi: b/t
}
```

Single dictionary with consistent value types
```
{/i
    i/123: 123
    f/123.456: t
}
```

Single dictionary with mixed key types
```
{
    i/123: s/Hello, world!
    s/hi: b/t
}
```

Single dictionary with consistent key and value types, with overloads
```
{i/i
    123: 11
    12: 32
    s/hi: b/t
}
```

List of dictionaries with consistent key types  # TODO
```
[
    /{
        i/123/s
        s/hi
    }
    {
        123: Hello, world!
        hi: b/t
    }
    {
        123: Hello, world!
        hi: f/1.2
    }
]
```

List of dictionaries with key aliases  # TODO
```
[
    /{
        i/my_very_long_key@0/s
        s/hi
    }
    {
        @0: Hello, world!
        hi: b/t
    }
    {
        @0: Bye, world!
        hi: f/1.2
    }
]
```
