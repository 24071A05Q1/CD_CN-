
#include <stdio.h>
#include <string.h>
#include <ctype.h>

char operand[50][50], op[50];
int top = -1, otop = -1, temp = 1;

int precedence(char ch)
{
    if (ch == '*' || ch == '/')
        return 2;
    if (ch == '+' || ch == '-')
        return 1;
    return 0;
}

void generate()
{
    char a[50], b[50], t[50];
    char oper = op[otop--];

    strcpy(b, operand[top--]);
    strcpy(a, operand[top--]);

    sprintf(t, "t%d", temp++);

    printf("%s = %s %c %s\n", t, a, oper, b);

    strcpy(operand[++top], t);
}

int main()
{
    char expr[100], s[50];
    int i, j;

    printf("Enter the expression: ");
    scanf("%s", expr);

    printf("\nThree Address Code:\n");

    for (i = 0; expr[i]; i++)
    {
        char ch = expr[i];

        if (isalnum(ch))
        {
            j = 0;

            while (isalnum(expr[i]))
                s[j++] = expr[i++];

            s[j] = '\0';
            strcpy(operand[++top], s);
            i--;
        }

        else if (ch == '(')
            op[++otop] = ch;

        else if (ch == ')')
        {
            while (op[otop] != '(')
                generate();

            otop--;
        }

        else
        {
            while (otop != -1 && op[otop] != '(' &&
                   precedence(op[otop]) >= precedence(ch))
                generate();

            op[++otop] = ch;
        }
    }

    while (otop != -1)
        generate();

    return 0;
}
