class solution:
    def countTriples(self, n: int) -> int:
        """Return the count of Pythagorean triples (ordered) with values <= n.

        This method preserves the original behavior: when a != b it counts
        both (a,b,c) and (b,a,c) as separate ordered triples.
        """
        count = 0
        for a in range(1, n + 1):
            for b in range(a, n + 1):
                c_square = a * a + b * b
                c = int(c_square ** 0.5)
                if c * c == c_square and c <= n:
                    if a == b:
                        count += 1
                    else:
                        count += 2
        return count


def triples_and_count(n: int, ordered: bool = True):
    """Return (count, triples) for Pythagorean triples with values <= n.

    - ordered=True: treat (a,b,c) and (b,a,c) as distinct (keeps original count semantics).
    - ordered=False: return unique unordered triples where a <= b (count equals number of unique triples).
    """
    triples = []
    unique = set()
    for a in range(1, n + 1):
        for b in range(a, n + 1):
            c_square = a * a + b * b
            c = int(c_square ** 0.5)
            if c * c == c_square and c <= n:
                if ordered:
                    if a == b:
                        triples.append((a, b, c))
                    else:
                        triples.append((a, b, c))
                        triples.append((b, a, c))
                else:
                    key = (a, b, c)  # since loop has a <= b, this is the canonical form
                    if key not in unique:
                        unique.add(key)
                        triples.append(key)

    count = len(triples)
    return count, triples


if __name__ == "__main__":
    # example usage
    n = 10

    # original count-only call (keeps backward compatibility)
    test = solution()
    print("Count (original method):", test.countTriples(n))

    # new function: ordered triples (keeps same counting semantics)
    count_ord, triples_ord = triples_and_count(n, ordered=True)
    print("\nOrdered triples count:", count_ord)
    print("Ordered triples:")
    for t in triples_ord:
        print(t)

    # new function: unique unordered triples
    count_unord, triples_unord = triples_and_count(n, ordered=False)
    print("\nUnique unordered triples count:", count_unord)
    print("Unique unordered triples:")
    for t in triples_unord:
        print(t)