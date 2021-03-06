from datetime import datetime, date


class Gympass:

    @staticmethod
    def make_dict(race_log):
        """
        This function searches on the log file for information to compose a dictionary with the race data.

        :return: a dictionary with ids of each pilot and them performance on race or a message that indicates a white
        log file.
        """
        with open(race_log) as race_log:
            race_log = race_log.readlines()

        race_log = [x.strip() for x in race_log][1:]

        if race_log:
            race = {}

            for i in race_log:
                i = i.replace('\t', ' ').replace(',', '.')
                i = i.split(' ')

                while '' in i:
                    i.remove('')

                if int(i[1]) not in race.keys():
                    race.update({int(i[1]): {'pilot_name': i[3]}})

                if int(i[4]) not in race[int(i[1])].keys():
                    race[int(i[1])].update({int(i[4]): {'hour': datetime.time(datetime.strptime(i[0], '%H:%M:%S.%f')),
                                                        'turn_time': datetime.combine(date.min,
                                                                                      datetime.time
                                                                                      (datetime.strptime(i[5],
                                                                                                         '%M:%S.%f')))
                                                                     - datetime.min, 'turn_speed': float(i[6])}})

            for i in race:
                pilot_time = datetime.min - datetime.min
                for j in race[i]:
                    if j is not 'pilot_name':
                        pilot_time = pilot_time + race[i][j]['turn_time']
                        turn_number = j
                race[i].update({'pilot_time': pilot_time,
                                'turn_number': turn_number})

            return race
        else:
            return 'O arquivo de log está em branco.'

    def order(self, race_log):
        """
        This function makes a dictionary ordered ascending by pilot_time

        :return: a dictionary with pilot's position on race or a message that indicates a white log file.
        """
        race = self.make_dict(race_log)

        if race == 'O arquivo de log está em branco.':
            return 'O arquivo de log está em branco.'

        else:
            order = {}

            date_pilot = {race[i]['pilot_time']: int(i) for i in race}
            ordered_date_pilot = sorted(date_pilot)

            for i in range(len(ordered_date_pilot)):
                order.update({i + 1: race[date_pilot[ordered_date_pilot[i]]]})

            return order

    def average_speed(self, race_log):
        """
        This function returns a dictionary with average speed of each pilot.

        :return: a dictionary with average speed of each pilot or a message that indicates a white log file.
        """
        race = self.make_dict(race_log)

        if race == 'O arquivo de log está em branco.':
            return 'O arquivo de log está em branco.'

        else:
            avg_speed = {}

            for i in race:
                avg_speed.update({int(i): []})
                for j in race[i]:
                    if j is not 'pilot_name' and j is not 'pilot_time' and j is not 'turn_number':
                        avg_speed[int(i)].append(race[i][j]['turn_speed'])
                avg_speed.update({int(i): float('{0:.3f}'.format(sum(avg_speed[i])/len(avg_speed[i])))})

            return avg_speed

    def output(self, race_log) -> str:
        """
        This function compose a txt file as output with the race results.

        :return: race result on a txt file, a message that indicates the race still didn't over  or a message that
        indicates a white log file.
        """

        race = self.make_dict(race_log)

        if race == 'O arquivo de log está em branco.':
            msg = 'O arquivo de log está em branco.'

        elif not max([race[i]['turn_number'] for i in race]) < 4:

            order = self.order(race_log)
            avg = self.average_speed(race_log)

            msg = ''

            for i in order:
                for j in race:
                    for k in avg:
                        if order[i]['pilot_name'] == race[j]['pilot_name'] and j == k:
                            msg = msg + 'O {}º colocado foi o piloto {} (ID: {}). Ele completou {} voltas, sendo que ' \
                                        'seu tempo total de prova foi {} e sua velocidade média foi {}\n'\
                                .format(i, race[j]['pilot_name'], j, race[j]['turn_number'], race[j]['pilot_time'],
                                        avg[k])

        else:
            msg = 'A corrida ainda não está finalizada, pois nenhum piloto completou 4 (quatro) voltas ainda.'

        with open('output.txt', 'w') as output:
            print(msg, file=output)

        return msg


Gympass().output('..\\gympass-test\\race_log.log')
