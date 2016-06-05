library(qcc)

plot.file <- 'plots.pdf'
file1 <- 'legs_2016_05.csv'
file2 <- 'legs_2016_06.csv'
name1 <- 'Mai/16'
name2 <- 'Jun/16'
cut <- 5

GetDelaysPerBase <- function(x, cutoff) {
    bases = c()
    count = c()
    for (org in levels(x$ORG)) {
        rows = nrow(x[x$ORG == org & x$CODE == 'TR' & x$ORG.DELAY > cutoff, ])
        if (rows > 0) {
            bases <- append(bases, org)
            count <- append(count, rows)
        }
    }
    names(count) <- bases
    return (count)
}

GetCnx <- function(x, base, cnx.type='PL') {
    return (x[x$ORG == base & x$PL.CNX <= 120, sprintf('%s.CNX', cnx.type)])
}

pdf(plot.file)

cnames <- c(
    "ROUTE",
    "FLEET",
    "NUMBER",
    "ORG",
    "DES",
    "SDT",
    "SAT",
    "P.BLOCK",
    "ADT",
    "AAT",
    "E.BLOCK",
    "CODE",
    "ORG.DELAY",
    "DES.DELAY",
    "PL.CNX",
    "PR.CNX",
    "EX.CNX"
)

x1 <- read.csv(file1, header=F, sep=';')
x2 <- read.csv(file2, header=F, sep=';')

colnames(x1) <- cnames
colnames(x2) <- cnames

d1 <- x1[x1$CODE == 'TR', 'ORG.DELAY']
d2 <- x2[x2$CODE == 'TR', 'ORG.DELAY']
cat('Atrasos na Origem')
print(t.test(d1, d2))
boxplot(d1, d2, names=c(name1, name2), col=c('orange', 'green'), 
    main='Atraso na Origem', ylab='Atraso (min)')

d1 <- GetDelaysPerBase(x1, cut)
d2 <- GetDelaysPerBase(x2, cut)

pareto.chart(d1, main=sprintf('Atrasos > %d min %s', cut, name1), ylab='Eventos', cex.names=0.8)
pareto.chart(d2, main=sprintf('Atrasos > %d min %s', cut, name2), ylab='Eventos', cex.names=0.8)

bases <- c(
    'CGH', 
    'GRU', 
    'BSB', 
    'GIG', 
    'SDU', 
    'POA', 
    'SSA',
    'REC'
)

for (org in bases) {
    pl1 <- GetCnx(x1, org, cnx.type='PL')
    pl2 <- GetCnx(x2, org, cnx.type='PL')
    pr1 <- GetCnx(x1, org, cnx.type='PR')
    pr2 <- GetCnx(x2, org, cnx.type='PR')
    n1 <- sprintf('Plan. %s', name1)
    n2 <- sprintf('Plan. %s', name2)
    n3 <- sprintf('Proj. %s', name1)
    n4 <- sprintf('Proj. %s', name2)
    cat(sprintf('Planejado %s', org))
    print(t.test(pl1, pl2))
    boxplot(pl1, pl2, pr1, pr2, names=c(n1, n2, n3, n4), 
        col=c('orange', 'green', 'gray', 'cyan'), 
        main=sprintf('Tempos de Solo %s', org), ylab='Tempo (min)')
}

dev.off()