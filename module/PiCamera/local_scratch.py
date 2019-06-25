def calculate_aspect(w, h):
    temp = 0

    def gcd(a, b):
        """GCD (greatest common divisor)"""
        return a if b == 0 else gcd(b, a % b)

    if w == h:
        return "1:1"

    if w < h:
        temp = w
        w = h
        h = temp

    gcd_divisor = gcd(w, h)

    x = int(w / gcd_divisor) if not temp else int(h / gcd_divisor)
    y = int(h / gcd_divisor) if not temp else int(w / gcd_divisor)

    return f"{x}:{y}"


z = calculate_aspect(1920, 1080)
print(z)
