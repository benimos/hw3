def readNumber(line, index):
    number = 0
    while index < len(line) and line[index].isdigit():
        number = number * 10 + int(line[index])
        index += 1
    if index < len(line) and line[index] == '.':
        index += 1
        keta = 0.1
        while index < len(line) and line[index].isdigit():
            number += int(line[index]) * keta
            keta *= 0.1
            index += 1
    token = {'type': 'NUMBER', 'number': number}
    return token, index


def readPlus(line, index):
    token = {'type': 'PLUS'}
    return token, index + 1


def readMinus(line, index):
    token = {'type': 'MINUS'}
    return token, index + 1

def readMultiply(line,index):
    token = {'type': 'MULTIPLY'}
    return token, index + 1

def readDivide(line,index):
    token = {'type': 'DIVIDE'}
    return token, index + 1


def tokenize(line):
    tokens = []
    index = 0
    global flag
    flag = 0
    while index < len(line):
        if line[index].isdigit():
            (token, index) = readNumber(line, index)
        elif line[index] == '+':
            (token, index) = readPlus(line, index)
        elif line[index] == '-':
            (token, index) = readMinus(line, index)
        elif line[index] == '*':
            (token, index) = readMultiply(line, index)
            flag += 1
        elif line[index] == '/':
            (token, index) = readDivide(line, index)
            flag += 1

        else:
            print('Invalid character found: ' + line[index])
            exit(1)
        tokens.append(token)
    return tokens


def evaluate(tokens):
    answer = 0
    index = 1
    tokens.insert(0, {'type': 'PLUS'}) # Insert a dummy '+' token
    if flag != 0:
        while index+1 < len(tokens):
            if tokens[index]['type'] == 'NUMBER':
                while tokens[index+1]['type'] == 'MULTIPLY' or tokens[index+1]['type'] == 'DIVIDE':
                    if tokens[index+1]['type'] == 'MULTIPLY':
                        tokens[index]['number'] = tokens[index]['number'] * tokens[index+2]['number']
                        tokens.pop(index+1)
                        tokens.pop(index+1)
                        index -= 2

                    elif tokens[index+1]['type'] == 'DIVIDE':
                        tokens[index]['number'] = (tokens[index]['number'] + 0.0) / tokens[index+2]['number']
                        tokens.pop(index+1)
                        tokens.pop(index+1)
                        index -= 2

                    index += 1
            index += 1

    index = 1
    while index < len(tokens):
        if tokens[index]['type'] == 'NUMBER':
            if tokens[index - 1]['type'] == 'PLUS':
                answer += tokens[index]['number']
            elif tokens[index - 1]['type'] == 'MINUS':
                answer -= tokens[index]['number']
            else:
                #print('Invalid syntax')
                print(tokens)
        index += 1
    return answer


def test(line, expectedAnswer):
    tokens = tokenize(line)
    actualAnswer = evaluate(tokens)
    if abs(actualAnswer - expectedAnswer) < 1e-8:
        print("PASS! (%s = %f)" % (line, expectedAnswer))
    else:
        print("FAIL! (%s should be %f but was %f)" % (line, expectedAnswer, actualAnswer))


# Add more tests to this function :)
def runTest():
    print("==== Test started! ====")
    test("1+2", 3)
    test("1.0+2.1-3", 0.1)
    test("3*2",6)
    test("1/2",0.5)
    test("2/0.2+1.2+3*4",23.2)
    print("==== Test finished! ====\n")

runTest()

while True:
    print('> '),
    line = input()
    tokens = tokenize(line)
    answer = evaluate(tokens)
    print("answer = %f\n" % answer)