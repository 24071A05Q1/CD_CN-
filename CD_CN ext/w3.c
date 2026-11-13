#include <stdio.h>
#include <string.h>

char lhs[10], rhs[10][10][10], first[10][20], follow[10][20];
int n, cnt[10];

void add(char s[], char c)
{
    if (!strchr(s, c))
    {
        int l = strlen(s);
        s[l] = c;
        s[l + 1] = '\0';
    }
}

int find(char c)
{
    for (int i = 0; i < n; i++)
        if (lhs[i] == c) return i;
    return -1;
}

int main()
{
    int i, j, k, x, ch;
    char t[100], *p;

    scanf("%d", &n);

    for (i = 0; i < n; i++)
    {
        scanf("%s", t);
        lhs[i] = t[0];
        p = strtok(strchr(t, '>') + 1, "|");

        while (p)
        {
            strcpy(rhs[i][cnt[i]++], p);
            p = strtok(NULL, "|");
        }
    }

    // FIRST
    do {
        ch = 0;
        for (i = 0; i < n; i++)
            for (j = 0; j < cnt[i]; j++)
            {
                char *s = rhs[i][j];
                int nul = 1;

                for (k = 0; s[k] && nul; k++)
                {
                    x = find(s[k]);

                    if (x == -1)
                    {
                        if (!strchr(first[i], s[k]))
                            add(first[i], s[k]), ch = 1;
                        nul = 0;
                    }
                    else
                    {
                        for (int z = 0; first[x][z]; z++)
                            if (first[x][z] != '#' &&
                                !strchr(first[i], first[x][z]))
                                add(first[i], first[x][z]), ch = 1;

                        if (!strchr(first[x], '#')) nul = 0;
                    }
                }

                if (nul && !strchr(first[i], '#'))
                    add(first[i], '#'), ch = 1;
            }
    } while (ch);

    // FOLLOW
    add(follow[0], '$');

    do {
        ch = 0;
        for (i = 0; i < n; i++)
            for (j = 0; j < cnt[i]; j++)
            {
                char *s = rhs[i][j];

                for (k = 0; s[k]; k++)
                {
                    x = find(s[k]);
                    if (x == -1) continue;

                    int nul = 1;

                    for (int z = k + 1; s[z] && nul; z++)
                    {
                        int y = find(s[z]);

                        if (y == -1)
                        {
                            if (!strchr(follow[x], s[z]))
                                add(follow[x], s[z]), ch = 1;
                            nul = 0;
                        }
                        else
                        {
                            for (int a = 0; first[y][a]; a++)
                                if (first[y][a] != '#' &&
                                    !strchr(follow[x], first[y][a]))
                                    add(follow[x], first[y][a]), ch = 1;

                            if (!strchr(first[y], '#')) nul = 0;
                        }
                    }

                    if (nul)
                        for (int a = 0; follow[i][a]; a++)
                            if (!strchr(follow[x], follow[i][a]))
                                add(follow[x], follow[i][a]), ch = 1;
                }
            }
    } while (ch);

    printf("\nFIRST SETS:\n");
    for (i = 0; i < n; i++)
        printf("FIRST(%c) = {%s}\n", lhs[i], first[i]);

    printf("\nFOLLOW SETS:\n");
    for (i = 0; i < n; i++)
        printf("FOLLOW(%c) = {%s}\n", lhs[i], follow[i]);
}