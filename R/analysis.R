library(qcc)

#### Entradas

args <- commandArgs(trailingOnly=T)

plot.file <- 'plots.pdf'
MONTHS <- c('Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun', 'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez')
WDAYS <- c('Dom', 'Seg', 'Ter', 'Qua', 'Qui', 'Sex', 'Sab')

if (length(args) != 7) {
    cat('Uso: Rscript analysis.R <legs1.csv> <name1> <mmyyyy> <legs2.csv> <name2> <mmyyyy> <cutoff>\n')
    stop()
} else {
    file1 <- args[1]
    name1 <- args[2]
    month1 <- as.integer(substr(args[3], 1, 2))
    year1 <- as.integer(substr(args[3], 3, 6))
    file2 <- args[4]
    name2 <- args[5]
    month2 <- as.integer(substr(args[6], 1, 2))
    year2 <- as.integer(substr(args[6], 3, 6))
    cutoff <- as.integer(args[7])
}

##### Funções

GetDelayTimes <- function(x, org=T, delay=T, cutoff=5, size=15) {
    bases = c()
    count = c()
    if (org) {
        list <- levels(x$ORG)
    } else {
        list <- levels(x$DES)   
    }
    for (b in list) {
        if (org) {
            rows <- ifelse(delay, nrow(x[x$ORG == b & x$ORG.DELAY > cutoff, ]), nrow(x[x$ORG == b & x$ORG.DELAY < -cutoff, ]))
        } else {
            rows <- ifelse(delay, nrow(x[x$DES == b & x$DES.DELAY > cutoff, ]), nrow(x[x$DES == b & x$DES.DELAY < -cutoff, ]))
        }
        if (rows > 0) {
            bases <- append(bases, b)
            count <- append(count, rows)
        }
    }
    names(count) <- bases
    return (sort(count, decreasing=T)[1:min(length(count), size)])
}

GetCnx <- function(x, base, cnx.type='PL') {
    return (x[x$ORG == base & x$PL.CNX <= 120, sprintf('%s.CNX', cnx.type)])
}

GetPeriodOrgDelay <- function(df, cutoff=5) {
    df$DAY <- as.Date(df$SDT, format='%d/%m/%y')
    days <- seq(from=min(df$DAY), to=max(df$DAY), by=1)
    x <- c()
    y <- c()
    for (i in 1:length(days)) {
        day <- days[i]
        flights <- nrow(df[df$DAY <= day, ])
        delayed <- nrow(df[df$DAY <= day & df$ORG.DELAY > cutoff, ])
        x[i] <- as.POSIXlt(day)$mday
        y[i] <- 100 * (1 - delayed / flights)
    }
    return (list(x, y))
}

GetDailyOrgDelay <- function(df, day, month, year, cutoff=5) {
    df$SDT.DT <- as.POSIXct(strptime(df$SDT, '%d/%m/%y %H:%M'), 'UTC')
    x <- c()
    y <- c()
    s <- sprintf('%02d/%02d/%04d 00:00', day, month, year)
    dt0 = as.POSIXct(strptime(s, '%d/%m/%Y %H:%M'), 'UTC')
    for (min in seq(0, 24 * 60, 30)) {
        s <- sprintf('%02d/%02d/%04d %02d:%02d', day, month, year, floor(min / 60), min %% 60)
        dt <- as.POSIXct(strptime(s, '%d/%m/%Y %H:%M'), 'UTC')
        flights <- nrow(df[df$SDT.DT >= dt0 & df$SDT.DT <= dt, ])
        delayed <- nrow(df[df$SDT.DT >= dt0 & df$SDT.DT <= dt & df$ORG.DELAY > cutoff, ])
        x <- append(x, min / 60)
        y <- append(y, 100 * (1 - delayed / flights))
    }
    return (list(x, y))
}

#### Inicialização

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

#### Atrasos na Saída

cat('==========================================================================\n')
cat('Atrasos na Saida\n')
cat('==========================================================================\n\n')

dep1 <- x1[x1$CODE == 'TR', 'ORG.DELAY']
dep2 <- x2[x2$CODE == 'TR', 'ORG.DELAY']
per1 <- 100 * length(dep1) / nrow(x1)
per2 <- 100 * length(dep2) / nrow(x2)
del1 <- sum(dep1) / nrow(x1)
del2 <- sum(dep2) / nrow(x1)
cat(sprintf('Total %s = %d (%5.2f%%)\n', name1, length(dep1), per1))
cat(sprintf('Total %s = %d (%5.2f%%) [Delta = %5.2f%%]\n', name2, length(dep2), per2, 100 * (per2 - per1) / per1))
cat(sprintf('Atrasado médio %s = %5.3f\n', name1, del1))
cat(sprintf('Atrasado médio %s = %5.3f [Delta = %5.2f%%]\n', name2, del2, 100 * (del2 - del1) / del1))
print(t.test(dep1, dep2))
boxplot(dep1, dep2, names=c(name1, name2), col=c('orange', 'green'), main='Atraso na Saida', ylab='Atraso (min)')
dep1 <- GetDelayTimes(x1, org=T, delay=T, cutoff=cutoff, size=15)
dep2 <- GetDelayTimes(x2, org=T, delay=T, cutoff=cutoff, size=15)
pareto.chart(dep1, main=sprintf('Atrasos > %d na Saída (%s)', cutoff, name1), ylab='Total', ylab2='', cex.names=0.8)
pareto.chart(dep2, main=sprintf('Atrasos > %d na Saída (%s)', cutoff, name2), ylab='Total', ylab2='', cex.names=0.8)

#### Atrasos na Chegada

cat('==========================================================================\n')
cat('Atrasos na Chegada\n')
cat('==========================================================================\n\n')

arr1 <- x1[x1$DES.DELAY > 0, 'DES.DELAY']
arr2 <- x2[x2$DES.DELAY > 0, 'DES.DELAY']
per1 <- 100 * length(arr1) / nrow(x1)
per2 <- 100 * length(arr2) / nrow(x2)
del1 <- sum(arr1) / nrow(x1)
del2 <- sum(arr2) / nrow(x2)
cat(sprintf('Total %s = %d (%5.2f%%)\n', name1, length(arr1), per1))
cat(sprintf('Total %s = %d (%5.2f%%) [Delta = %5.2f%%]\n', name2, length(arr2), per2, 100 * (per2 - per1) / per1))
cat(sprintf('Atrasado médio %s = %5.3f\n', name1, del1))
cat(sprintf('Atrasado médio %s = %5.3f [Delta = %5.2f%%]\n', name2, del2, 100 * (del2 - del1) / del1))
print(t.test(arr1, arr2))
boxplot(arr1, arr2, names=c(name1, name2), col=c('orange', 'green'), main='Atraso na Chegada', ylab='Atraso (min)')
arr1 <- GetDelayTimes(x1, org=F, delay=T, cutoff=cutoff, size=15)
arr2 <- GetDelayTimes(x2, org=F, delay=T, cutoff=cutoff, size=15)
pareto.chart(arr1, main=sprintf('Atrasos > %d na Chegada (%s)', cutoff, name1), ylab='Total', ylab2='', cex.names=0.8)
pareto.chart(arr2, main=sprintf('Atrasos > %d na Chegada (%s)', cutoff, name2), ylab='Total', ylab2='', cex.names=0.8)

#### Atrasos na Chegada

cat('==========================================================================\n')
cat('Antecipações na Chegada\n')
cat('==========================================================================\n\n')

arr1 <- x1[x1$DES.DELAY < 0, 'DES.DELAY']
arr2 <- x2[x2$DES.DELAY < 0, 'DES.DELAY']
per1 <- 100 * length(arr1) / nrow(x1)
per2 <- 100 * length(arr2) / nrow(x2)
ant1 <- sum(arr1) / nrow(x1)
ant2 <- sum(arr2) / nrow(x2)
cat(sprintf('Total %s = %d (%5.2f%%)\n', name1, length(arr1), per1))
cat(sprintf('Total %s = %d (%5.2f%%) [Delta = %5.2f%%]\n', name2, length(arr2), per2, 100 * (per2 - per1) / per1))
cat(sprintf('Antecipação média %s = %5.3f\n', name1, ant1))
cat(sprintf('Antecipação média %s = %5.3f [Delta = %5.2f%%]\n', name2, ant2, 100 * (ant2 - ant1) / del1))
print(t.test(arr1, arr2))
boxplot(arr1, arr2, names=c(name1, name2), col=c('orange', 'green'), main='Antecipação na Chegada', ylab='Antecipação (min)')
arr1 <- GetDelayTimes(x1, org=F, delay=F, cutoff=cutoff, size=15)
arr2 <- GetDelayTimes(x2, org=F, delay=F, cutoff=cutoff, size=15)
pareto.chart(arr1, main=sprintf('Antecipações < -%d na Chegada (%s)', cutoff, name1), ylab='Total', ylab2='', cex.names=0.8)
pareto.chart(arr2, main=sprintf('Antecipações < -%d na Chegada (%s)', cutoff, name2), ylab='Total', ylab2='', cex.names=0.8)

#### Tempos de Solo

cat('==========================================================================\n')
cat('Tempos de Solo\n')
cat('==========================================================================\n\n')

bases <- c(
    'CGH', 
    'GRU',  
    'GIG', 
    'SDU',
    'BSB',
    'POA'
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

#### Pontualidade mensal

d1 <- GetPeriodOrgDelay(x1, cutoff=cutoff)
d2 <- GetPeriodOrgDelay(x2, cutoff=cutoff)
plot(d1[[1]], d1[[2]], main=sprintf('Pontualidade no Período [%d minutos]', cutoff), 
    ylim=c(80, 100), col='red', type='o', ylab='Pontualidade (%)', xlab='Dia do Mês')
text(d1[[1]], d1[[2]], sprintf('%3.1f', d1[[2]]), pos=3, cex=0.5)
par(new=T) 
plot(d2[[1]], d2[[2]], 
    ylim=c(80, 100), col='blue', type='o', axes=F, xlab='', ylab='')
text(d2[[1]], d2[[2]], sprintf('%3.1f', d2[[2]]), pos=3, cex=0.5)
legend("topleft", legend=c(name1, name2), col=c('red', 'blue'), lty=c(1, 1), cex=0.8)

#### Pontualidade diária

# Consertar
for (i in 1:30) {
    day <- i
    cat(sprintf('Plotando pontualidade dia %02d...\n', day))
    d1 <- GetDailyOrgDelay(x1, day=day, month=month1, year=year1, cutoff=cutoff)
    d2 <- GetDailyOrgDelay(x2, day=day, month=month2, year=year2, cutoff=cutoff)
    plot(d1[[1]], d1[[2]], main=sprintf('Pontualidade Dia %02d [%d minutos]', day, cutoff), 
        ylim=c(70, 100), type='o', col='red', axes=F, ylab='Pontualidade (%)', xlab='Hora do Dia')
    axis(1, at=seq(0, 24, 1))
    axis(2)
    box()
    par(new=T) 
    plot(d2[[1]], d2[[2]], 
        ylim=c(70, 100), type='o', col='blue', axes=F, ylab='', xlab='')
    wday1 <- WDAYS[as.POSIXlt(ISOdate(year1, month1, day))$wday + 1]
    wday2 <- WDAYS[as.POSIXlt(ISOdate(year2, month2, day))$wday + 1]
    legend("topright", legend=c(sprintf('%s (%s)', name1, wday1), sprintf('%s (%s)', name2, wday2)), 
        col=c('red', 'blue'), lty=c(1, 1), cex=0.8)
}

dev.off()