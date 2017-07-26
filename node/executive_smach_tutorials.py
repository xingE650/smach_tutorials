#!/usr/bin/env python

import roslib; roslib.load_manifest('smach_tutorials')
import rospy
import smach
import smach_ros

# define state Foo
class Foo(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome1','outcome2'],
                             input_keys=['foo_counter_in'],
                             io_keys=['foo_counter_out'])
        self.mode =True

    def execute(self, userdata):
        rospy.loginfo('Executing state FOO')
        try:
            getattr(userdata, 'foo_counter_in')
        except:
            rospy.loginfo('fuck')
            # raise KeyboardInterrupt
            return 'outcome2'

        # if 'foo_counter_in' not in key_lists:
        #     return 'outcome1'
        # else:
        if userdata.foo_counter_in < 4:
            userdata.foo_counter_out = userdata.foo_counter_in + 1 
            self.foo_counter_out =userdata.foo_counter_out
            self.mode =not self.mode
            if self.mode ==False: 
                rospy.logerr(str(self.foo_counter_out))
            return 'outcome1'
        else:
            return 'outcome2'


# define state Bar
class Bar(smach.State):
    def __init__(self):
        smach.State.__init__(self, 
                             outcomes=['outcome1'],
                             input_keys=['sentences'])
        
    def execute(self, userdata):
        rospy.loginfo('Executing state BAR')
        print userdata.sentences    
        return 'outcome1'
        




def main():
    rospy.init_node('smach_example_state_machine')
    # no data communicate may be error as unavailable keys
    # Create a SMACH state machine
    hehe =4.0
    sm = smach.StateMachine(outcomes=['outcome4'],
                            output_keys =['sm_out'])
    
    # print 'sm has the userdata keys' + str(sm.userdata.keys())
    # only after instance the keys , the userdata will have the keys
    # Open the container
    # python varible is regarded as a label
    # so if you change the same userdata in the statemachine it may use the last value
    with sm:
        sm.userdata.sm_counter =1
        sm.userdata.sm_out = 'hehe_fuckyou'
        # Add states to the container
        smach.StateMachine.add('FOO', Foo(), 
                               transitions={'outcome1':'BAR', 
                                            'outcome2':'outcome4'},
                                remapping ={'foo_counter_in':'sm_counter','foo_counter_out':'sm_counter'}
                                )
        smach.StateMachine.add('BAR', Bar(), 
                               transitions={'outcome1':'FOO'},
                               remapping={'sentences':'sm_out'})
        
        # smach.StateMachine.add('FOO_1',Foo(),
        #                         transitions ={'outcome1':'outcome4',
        #                                         'outcome2':'outcome4'},
        #                         remapping ={'foo_counter_in':'sm_counter','foo_counter_out':'sm_counter'})
       
    # Execute SMACH plan
    outcome = sm.execute()
   

if __name__ == '__main__':
    main()