
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main()
{
    FILE *fp;
    char file[50], word[50], num[50], ch;
    int i;

    printf("Enter file name: ");
    scanf("%s", file);

    fp = fopen(file, "r");

    if (fp == NULL)
    {
        printf("File not found");
        return 0;
    }

    while ((ch = fgetc(fp)) != EOF)
    {
        if (isalpha(ch) || ch == '_')
        {
            i = 0;
            word[i++] = ch;

            while (isalnum(ch = fgetc(fp)) || ch == '_')
                word[i++] = ch;

            word[i] = '\0';
            ungetc(ch, fp);

            if (strcmp(word, "int") == 0 ||
                strcmp(word, "float") == 0 ||
                strcmp(word, "if") == 0 ||
                strcmp(word, "else") == 0 ||
                strcmp(word, "return") == 0)
                printf("KEY: %s\n", word);
            else
                printf("IDF: %s\n", word);
        }
        else if (isdigit(ch))
        {
            i = 0;
            num[i++] = ch;

            while (isdigit(ch = fgetc(fp)))
                num[i++] = ch;

            num[i] = '\0';
            ungetc(ch, fp);

            printf("NUMBER: %s\n", num);
        }
        else if (ch == '+' || ch == '-' ||
                 ch == '/' || ch == '*' || ch == '=')
        {
            printf("OPERATOR: %c\n", ch);
        }
        else if (ch == '(' || ch == ')' ||
                 ch == '{' || ch == '}' ||
                 ch == ';' || ch == ',')
        {
            printf("DELIMITER: %c\n", ch);
        }
        else if (isspace(ch))
        {
            continue;
        }
        else
        {
            i = 0;
            word[i++] = ch;

            while ((ch = fgetc(fp)) != EOF &&
                   !isspace(ch) &&
                   ch != '+' && ch != '-' &&
                   ch != '*' && ch != '/' && ch != '=' &&
                   ch != '(' && ch != ')' &&
                   ch != '{' && ch != '}' &&
                   ch != ';' && ch != ',')
            {
                word[i++] = ch;
            }

            word[i] = '\0';

            if (ch != EOF)
                ungetc(ch, fp);

            printf("INVALID TOKEN: %s\n", word);
        }
    }

    fclose(fp);
    return 0;
}
