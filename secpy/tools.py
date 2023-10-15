from secpy.financials.tools import get_financials
from secpy.financials.utils import filter_earlier_values_from_financial, filter_earlier_values_from_list
import matplotlib.pyplot as plt
import json
# import matplotlib
# matplotlib.use('TkAgg')

def generate_financials(client,ticker,start_year,save_dir,save,plot,overwrite):
    financials,all_end_dates = get_financials(client,ticker)

    for financial_key, financial in financials.items():
        # if financial_key in ['balance_sheet','income_statement']:
        #     continue

        if save:
            with open(save_dir/f'{financial_key}.csv','w') as f:
                json.dump(financial,f)

        if plot:

            # apply start_year before plotting
            if start_year:
                financial = filter_earlier_values_from_financial(financial,start_year)
                all_end_dates = filter_earlier_values_from_list(all_end_dates,start_year)

            fig,ax=plt.subplots(len(financial),sharex=True)
            plt.xticks(rotation=45)
            plt.subplots_adjust(hspace=1.25)  # You can adjust the hspace value
            for i, (key, financial_dict) in enumerate(financial.items()):
                ax[i].tick_params(axis='x', labelsize=6)
                ax[i].tick_params(axis='y', labelsize=6)  
                financial_dict_with_all_dates = {end:0 for end in all_end_dates}
                for end, values in financial_dict.items():
                    financial_dict_with_all_dates[end] = values[0]

                # Remove zeros
                hard_number_keys = [] # Not ratios like Earnings Per Share
                for end,value in financial_dict_with_all_dates.items():
                    if (value>1e6) or (value<-1e6):
                        hard_number_keys.append(key)
                        break
                is_hard_number_key = key in hard_number_keys 
                if is_hard_number_key:
                    ax[i].set_title(f"{key} (in Millions)", fontsize=10)
                else:
                    ax[i].set_title(key, fontsize=10)
                # Plot
                for ii, (end, value) in enumerate(financial_dict_with_all_dates.items()):
                    if is_hard_number_key:
                        plot_value = value/1e6
                    else:
                        plot_value = value

                    if value >= 0:
                        color = 'blue'
                        text_level = plot_value + 0.1
                    else:
                        color = 'red'
                        text_level =  - plot_value - 0.1

                    #     ax[i].bar(x=key,height=value,color='red')
                    #     ax[i].text(ii, - value - 0.1, str("{:.1e}".format(value)), ha='center', va='bottom')
                    
                    ax[i].bar(x=end,height=plot_value,color=color)
                    ax[i].text(ii, text_level, str(round(plot_value,2)), ha='center', va='bottom', fontsize=6)
                    

            # plt.savefig(str(save_dir / f'{financial_key}.png'))
            plt.show()